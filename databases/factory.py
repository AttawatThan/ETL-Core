from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type
from airflow.providers.common.sql.hooks.sql import DbApiHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.exceptions import AirflowNotFoundException
from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from etl_core.utils.log_util import setup_logging

logger = setup_logging(__name__)


class DatabaseStrategy(ABC):
    """Abstract base class defining the interface for database connection strategies.
    
    This class enforces a standard workflow for creating and validating database 
    engines. Subclasses must implement the `create_hook` method to provide the 
    specific Airflow Hook for their database type.
    """

    @abstractmethod
    def create_hook(self, conn_id: str, hook_options: Dict[str, Any]) -> DbApiHook:
        """Instantiates the specific Airflow Hook for the database type.

        Args:
            conn_id: The Airflow connection ID to retrieve credentials from.
            hook_options: A dictionary of additional keyword arguments to pass 
                to the Hook's constructor (e.g., schema, timeout).

        Returns:
            An instance of a class inheriting from airflow.providers.common.sql.hooks.sql.DbApiHook.
        """
        pass
    
    def create_validated_engine(
        self, 
        conn_id: str, 
        hook_options: Dict[str, Any], 
        sqlalchemy_options: Dict[str, Any]
    ) -> Engine:
        """Creates a SQLAlchemy engine and validates the connection.

        This method acts as a template, orchestrating the creation of the hook,
        retrieval of the engine, and execution of a 'SELECT 1' liveness check.

        Args:
            conn_id: The Airflow connection ID. Cannot be None or empty.
            hook_options: Options passed to the Airflow Hook constructor.
            sqlalchemy_options: Options passed to the SQLAlchemy engine creation 
                (e.g., pool_size, isolation_level).

        Returns:
            A SQLAlchemy Engine object that has been successfully tested.

        Raises:
            ValueError: If `conn_id` is None or empty.
            AirflowNotFoundException: If the `conn_id` does not exist in Airflow.
            SQLAlchemyError: If the engine cannot be created or the connection 
                validation fails.
        """
        if not conn_id or not conn_id.strip():
            raise ValueError("Connection ID (conn_id) cannot be None or empty.")

        try:
            # Create the hook with specific options
            hook = self.create_hook(conn_id, hook_options)
            
            # Retrieve engine using the hook, passing sqlalchemy options
            engine = hook.get_sqlalchemy_engine(engine_kwargs=sqlalchemy_options)
            
            logger.info("Successfully created engine for connection: '%s'", conn_id)

            # Validate the connection immediately
            self._validate_connection(engine, conn_id)
            
            return engine

        except AirflowNotFoundException:
            logger.error("Airflow connection ID '%s' not found.", conn_id)
            raise
        except SQLAlchemyError as err:
            logger.error("Failed to create or validate engine for '%s'. Error: %s", conn_id, err)
            raise
    
    def _validate_connection(self, engine: Engine, conn_id: str) -> None:
        """Executes a lightweight query to verify database connectivity.

        Args:
            engine: The SQLAlchemy Engine to test.
            conn_id: The connection ID (used for logging context).

        Raises:
            SQLAlchemyError: If the 'SELECT 1' query fails.
        """
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            logger.debug("Connection test passed for '%s'.", conn_id)
        except Exception as err:
            raise SQLAlchemyError(f"Connection test failed: {err}")


class PostgresStrategy(DatabaseStrategy):
    """Strategy implementation for PostgreSQL databases."""

    def create_hook(self, conn_id: str, hook_options: Dict[str, Any]) -> PostgresHook:
        """Creates a PostgresHook instance.

        Args:
            conn_id: The Airflow connection ID.
            hook_options: Additional arguments for PostgresHook (e.g., schema).

        Returns:
            A configured PostgresHook.
        """
        return PostgresHook(postgres_conn_id=conn_id, **hook_options)


class MsSqlStrategy(DatabaseStrategy):
    """Strategy implementation for Microsoft SQL Server databases."""

    def create_hook(self, conn_id: str, hook_options: Dict[str, Any]) -> MsSqlHook:
        """Creates a MsSqlHook instance.

        Args:
            conn_id: The Airflow connection ID.
            hook_options: Additional arguments for MsSqlHook.

        Returns:
            A configured MsSqlHook instance.
        """
        return MsSqlHook(mssql_conn_id=conn_id, **hook_options)



class DatabaseEngineFactory:
    """Factory class for creating database engines based on registered strategies.

    This class maintains a registry of supported database types and their 
    corresponding strategies. It serves as the single entry point for client code 
    to request database connections.
    """
    
    _registry: Dict[str, Type[DatabaseStrategy]] = {}

    @classmethod
    def register_strategy(cls, db_type: str, strategy_cls: Type[DatabaseStrategy]) -> None:
        """Registers a new database strategy.

        Args:
            db_type: A string identifier for the database (e.g., 'postgres'). 
                Case-insensitive.
            strategy_cls: The class implementing DatabaseStrategy.
        """
        cls._registry[db_type.lower()] = strategy_cls

    @classmethod
    def get_engine(
        cls, 
        db_type: str, 
        conn_id: str, 
        hook_options: Optional[Dict[str, Any]] = None, 
        sqlalchemy_options: Optional[Dict[str, Any]] = None
    ) -> Engine:
        """Retrieves a validated SQLAlchemy Engine for the specified database type.

        Args:
            db_type: The type of database to connect to (e.g., 'postgres', 'mssql').
            conn_id: The Airflow connection ID.
            hook_options: Optional dictionary of arguments for the Airflow Hook.
                Defaults to an empty dict.
            sqlalchemy_options: Optional dictionary of arguments for the 
                SQLAlchemy engine. Defaults to an empty dict.

        Returns:
            A validated SQLAlchemy Engine ready for use.

        Raises:
            ValueError: If `db_type` is not supported (not registered).
            AirflowNotFoundException: If `conn_id` is missing in Airflow.
            SQLAlchemyError: If connection validation fails.
        """
        hook_options = hook_options or {}
        sqlalchemy_options = sqlalchemy_options or {}

        strategy_cls = cls._registry.get(db_type.lower())
        
        if not strategy_cls:
            valid_types = list(cls._registry.keys())
            raise ValueError(
                f"Unsupported database type: '{db_type}'. "
                f"Supported types: {valid_types}"
            )
        
        strategy = strategy_cls()
        return strategy.create_validated_engine(conn_id, hook_options, sqlalchemy_options)


# --- Configuration / Registration ---
# Register supported strategies upon module import
DatabaseEngineFactory.register_strategy('postgres', PostgresStrategy)
DatabaseEngineFactory.register_strategy('mssql', MsSqlStrategy)

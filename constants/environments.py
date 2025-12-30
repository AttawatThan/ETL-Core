"""Environment constants.

This module defines the Environment enumeration used to identify
different deployment environments within the ETL pipeline.
"""

from enum import StrEnum


class Environment(StrEnum):
    """Enumeration of deployment environments.

    Attributes:
        LOCAL: Local development environment.
        DEVELOPMENT: Development environment.
        UAT: User Acceptance Testing environment.
        PREPRODUCTION: Pre-production environment.
        PRODUCTION: Production environment.
    """

    LOCAL = 'local'
    DEVELOPMENT = 'development'
    UAT = 'uat'
    PREPRODUCTION = 'preproduction'
    PRODUCTION = 'production'

"""Audit field constants.

This module defines the AuditField enumeration used for tracking
creation and update information in the ETL pipeline.
"""

from enum import StrEnum


class AuditField(StrEnum):
    """Enumeration of audit fields.

    Attributes:
        CREATED_BY_SYSTEM: Default value for the created_by field.
        UPDATED_BY_SYSTEM: Default value for the updated_by field.
    """

    CREATED_BY_SYSTEM = "system"
    UPDATED_BY_SYSTEM = "system"
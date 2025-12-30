from constants.audit_fields import AuditField


def test_audit_field_values():
    """Test that AuditField enum members have correct values."""
    assert AuditField.CREATED_BY_SYSTEM == "system"
    assert AuditField.UPDATED_BY_SYSTEM == "system"

def test_audit_field_members():
    """Test that AuditField enum has all expected members."""
    members = AuditField.__members__
    assert "CREATED_BY_SYSTEM" in members
    assert "UPDATED_BY_SYSTEM" in members
    assert len(members) == 2

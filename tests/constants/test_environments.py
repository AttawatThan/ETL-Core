from constants.environments import Environment


def test_environment_values():
    """Test that Environment enum members have correct values."""
    assert Environment.LOCAL == 'local'
    assert Environment.DEVELOPMENT == 'development'
    assert Environment.UAT == 'uat'
    assert Environment.PREPRODUCTION == 'preproduction'
    assert Environment.PRODUCTION == 'production'

def test_environment_members():
    """Test that Environment enum has all expected members."""
    members = Environment.__members__
    assert 'LOCAL' in members
    assert 'DEVELOPMENT' in members
    assert 'UAT' in members
    assert 'PREPRODUCTION' in members
    assert 'PRODUCTION' in members
    assert len(members) == 5

"""Test the settings validator."""
from ou_container_content.validator import validate_settings


def test_null_settings():
    """Test that null settings are correctly coerced."""
    result = validate_settings(None)
    assert result == {}


def test_empty_settings():
    """Test that empty settings are accepted."""
    settings = {}
    result = validate_settings(settings)
    assert result == {}

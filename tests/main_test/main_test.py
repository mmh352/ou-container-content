"""Tests for the commandline interface."""
import os

from click.testing import CliRunner

from ou_container_content.__main__ import main


def test_basic_copy():
    """Test that the basic CLI works."""
    config_filename = os.path.join(os.getcwd(), os.path.dirname(__file__), 'config.yaml')
    runner = CliRunner()
    result = runner.invoke(main, ['-c', config_filename, 'startup'])
    assert result.exit_code == 0


def test_fail_missing_config():
    """Test that a missing configuration file fails."""
    config_filename = os.path.join(os.getcwd(), os.path.dirname(__file__), 'missing-config.yaml')
    runner = CliRunner()
    result = runner.invoke(main, ['-c', config_filename, 'startup'])
    assert result.exit_code == 2

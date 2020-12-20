# pylint: disable=unused-argument
"""Functional tests."""
from fm_database.settings import DevConfig, ProdConfig, TestConfig, get_config


def test_retrieving_settings():
    """Test that the correct settings are retrieved."""
    test_config = get_config(override_default="test")
    dev_config = get_config(override_default="dev")
    prod_config = get_config(override_default="prod")
    wrong_config = get_config(override_default="wrong")
    default_config = get_config()

    assert test_config == TestConfig
    assert dev_config == DevConfig
    assert prod_config == ProdConfig
    assert wrong_config == DevConfig
    assert default_config == DevConfig

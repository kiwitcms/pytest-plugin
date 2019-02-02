# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
import configparser
import os

import attr
import pytest

DEFAULT_CONFIG_PATH = "~/.tcms.conf"


def pytest_addoption(parser):
    group = parser.getgroup("kiwitcms")
    group.addoption(
        "--kiwitcms", action="store_true", help="Enable recording of test results in Kiwi TCMS."
    )


def pytest_configure(config):
    if config.getoption("--kiwitcms"):
        config_manager = ConfigManager(config)
        config.pluginmanager.register(
            Plugin(
                api_url=config_manager.get_option("url", "TCMS_API_URL"),
                username=config_manager.get_option("username", "TCMS_USERNAME"),
                password=config_manager.get_option("password", "TCMS_PASSWORD"),
            ),
            name="pytest-kiwitcms",
        )


def is_not_none(instance, attribute, value):  # pylint: disable=unused-argument
    if not value:
        pytest.exit(msg=f"Option {attribute.name} is empty", returncode=1)


@attr.s(hash=True)
class Plugin:  # pylint: disable=too-few-public-methods
    api_url = attr.ib(type=str, validator=is_not_none)
    username = attr.ib(type=str, validator=is_not_none)
    password = attr.ib(type=str, validator=is_not_none)


@attr.s
class ConfigManager:  # pylint: disable=too-few-public-methods
    """Helper for configuration parsing."""

    pytest_config = attr.ib()
    config_file = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.config_file = configparser.ConfigParser()
        self.config_file.read(os.path.expanduser(DEFAULT_CONFIG_PATH))

    def get_option(self, config_name, envvar):
        try:
            return self.config_file["tcms"][config_name]
        except KeyError:
            return os.getenv(envvar)

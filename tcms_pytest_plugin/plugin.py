# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
import configparser
import os
from typing import Dict

import attr
import pytest
import tcms_api

DEFAULT_CONFIG_PATH = "~/.tcms.conf"


def pytest_addoption(parser):
    group = parser.getgroup("kiwitcms")
    group.addoption(
        "--kiwitcms", action="store_true", help="Enable recording of test results in Kiwi TCMS."
    )


#
#
# test_plan = rpc_client.TestPlan.create({
#     'name': 'Performance baseline TP at %s' % NOW,
#     'text': 'A script is creating this TP and adds TCs and TRs to it to eastablish a performance baseline',
#     'type': 7, # Performance
#     'product': PRODUCT_ID,
#     'product_version': PRODUCT_VERSION,
#     'is_active': True,
# })
#
# test_cases = []
# for case in TEST_CASES_250:
#     test_case = rpc_client.TestCase.create({
#         'summary': '%s at %s' % (case, NOW),
#         'product': PRODUCT_ID,
#         'category': CATEGORY_ID,
#         'priority': PRIORITY_ID,
#         'case_status': 2, # CONFIRMED
#     })
#     test_cases.append(test_case)
#
#     rpc_client.TestPlan.add_case(test_plan['plan_id'], test_case['case_id'])
#
#
# build = rpc_client.Build.create({
#     'name': 'b.%s' % NOW,
#     'description': 'the product build at %s' % NOW,
#     'product': PRODUCT_ID,
# })
#
# test_run = rpc_client.TestRun.create({
#     'summary': 'Performance baseline at %s' % NOW,
#     'manager': 'atodorov',
#     'plan': test_plan['plan_id'],
#     'build': build['build_id'],
# })

import os, ssl

# if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(ssl, "_create_unverified_context", None):
#     ssl._create_default_https_context = ssl._create_unverified_context


def pytest_configure(config):
    if config.getoption("--kiwitcms"):
        config_manager = ConfigManager()
        config.pluginmanager.register(
            Plugin(
                api_url=config_manager.get_option("url", "TCMS_API_URL"),
                username=config_manager.get_option("username", "TCMS_USERNAME"),
                password=config_manager.get_option("password", "TCMS_PASSWORD"),
                product=config_manager.get_env_option(
                    "TCMS_PRODUCT", "TRAVIS_REPO_SLUG", "JOB_NAME"
                ),
                product_version=config_manager.get_env_option(
                    "TCMS_PRODUCT_VERSION", "TRAVIS_COMMIT", "TRAVIS_PULL_REQUEST_SHA", "GIT_COMMIT"
                ),
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

    product = attr.ib()
    product_version = attr.ib()

    use_mod_kerb = attr.ib(type=bool, default=False)

    @property
    def rpc(self):
        if not hasattr(self, "_connection"):
            if self.use_mod_kerb:
                # use Kerberos
                self._rpc = tcms_api.TCMSKerbXmlrpc(self.api_url).server
            else:
                # use plain authentication otherwise
                self._rpc = tcms_api.TCMSXmlrpc(self.username, self.password, self.api_url).server
        return self._rpc

    @property
    def product_obj(self):
        if not hasattr(self, "_product_obj"):
            # maybe ID is passed
            try:
                self._product_obj = self.rpc.Product.filter({"id": self.product})[0]
            except Exception:  # replace with RPC error
                try:
                    self._product_obj = self.rpc.Product.filter({"name": self.product})[0]
                except Exception:
                    # classification_id ?
                    self._product_obj = self.rpc.Product.create(
                        {"name": self.product, "classification_id": 1}
                    )
        return self._product_obj

    def create_test_plan(self):
        self.test_plan = self.rpc.TestPlan.create(
            {
                "name": f"Automated test plan for {self.product}",
                "product": self.product_id,
                "product_version": self.product_version,
                "type": 1,  # Unit
            }
        )
        return self.test_plan

    # Hooks implementation
    @pytest.hookimpl(trylast=True)
    def pytest_collection_modifyitems(self, session, config, items):
        self.create_test_plan()


@attr.s
class ConfigManager:  # pylint: disable=too-few-public-methods
    """Helper for configuration parsing."""

    config_file = attr.ib(init=False)

    def __attrs_post_init__(self):
        """Configuration file parsing.

        Having it on the instance level simplifies testing - it allows to reconfigure $HOME variable before
        loading the plugin.
        """
        self.config_file = configparser.ConfigParser()
        self.config_file.read(os.path.expanduser(DEFAULT_CONFIG_PATH))

    def get_option(self, config_name, envvar):
        """Return the `config_name` value from the config file.

        Fallback to environment variable value if config doesn't contain the given key.
        """
        try:
            return self.config_file["tcms"][config_name]
        except KeyError:
            return os.getenv(envvar)

    def get_env_option(self, *aliases):
        """Return the first available environment variable value from the given aliases."""
        for alias in aliases:
            try:
                return os.environ[alias]
            except KeyError:
                continue


# TODO.
# 1. Load variables for TCMS_PRODUCT, etc
# 2. Create TestPlan & TestRun
# 3. Check for TCMS_RUN_ID
# 4. Check if product, version, build exist
#
#
#

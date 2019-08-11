# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
import pytest


pytestmark = pytest.mark.vcr

DEFAULT_CONFIG = (
    ("TCMS_API_URL", "http://another.com/xml-rpc/"),
    ("TCMS_USERNAME", "user"),
    ("TCMS_PASSWORD", "random"),
)


@pytest.mark.usefixtures("config_file")
def test_file_configuration(testdir, tcms_api_url, tcms_username, tcms_password):
    """Load configuration from ~/.tcms.conf."""
    testdir.makepyfile(
        f"""
        def test_file_configuration(pytestconfig):
            plugin = pytestconfig.pluginmanager.get_plugin("pytest-kiwitcms")
            assert plugin.api_url == "{tcms_api_url}"
            assert plugin.username == "{tcms_username}"
            assert plugin.password == "{tcms_password}"
    """
    )
    result = testdir.runpytest("--kiwitcms", "-v")
    result.stdout.fnmatch_lines(["*::test_file_configuration PASSED*"])
    assert result.ret == 0


def test_env_configuration(testdir, monkeypatch):
    """If ~/.tcms.conf doesn't exist - use env variables."""
    for envvar, value in DEFAULT_CONFIG:
        monkeypatch.setenv(envvar, value)
    testdir.makepyfile(
        """
        def test_env_configuration(pytestconfig):
            plugin = pytestconfig.pluginmanager.get_plugin("pytest-kiwitcms")
            assert plugin.api_url == "http://another.com/xml-rpc/"
            assert plugin.username == "user"
            assert plugin.password == "random"
        """
    )
    result = testdir.runpytest("--kiwitcms", "-v")
    result.stdout.fnmatch_lines(["*::test_env_configuration PASSED*"])
    assert result.ret == 0


@pytest.mark.parametrize("envvar, value", DEFAULT_CONFIG, ids=["url", "username", "password"])
@pytest.mark.usefixtures("config_file")
def test_config_file_precedence(
    testdir, monkeypatch, envvar, value, tcms_api_url, tcms_username, tcms_password
):
    """Values from ~/.tcms.conf have higher priority than env variables."""
    monkeypatch.setenv(envvar, value)
    testdir.makepyfile(
        f"""
        def test_config_file_precedence(pytestconfig):
            plugin = pytestconfig.pluginmanager.get_plugin("pytest-kiwitcms")
            assert plugin.api_url == "{tcms_api_url}"
            assert plugin.username == "{tcms_username}"
            assert plugin.password == "{tcms_password}"
        """
    )
    result = testdir.runpytest("--kiwitcms", "-v")
    result.stdout.fnmatch_lines(["*::test_config_file_precedence PASSED*"])
    assert result.ret == 0


def test_empty_variable(testdir):
    """Any empty value in config variables will lead to program exiting."""
    testdir.makepyfile(
        """
        def test_empty_variable(pytestconfig):
            plugin = pytestconfig.pluginmanager.get_plugin("pytest-kiwitcms")
        """
    )
    result = testdir.runpytest("--kiwitcms", "-v")
    result.stderr.fnmatch_lines(["Exit: Option api_url is empty"])
    assert result.ret == 1


@pytest.mark.parametrize(
    "product_key, product, product_version_key, product_version",
    (
        ("TCMS_PRODUCT", "31", "TCMS_PRODUCT_VERSION", "721"),
        (
            "TRAVIS_REPO_SLUG",
            "kiwitcms",
            "TRAVIS_COMMIT",
            "edfd072fd323ea717337407aeb7134c9e8884368",
        ),
        (
            "JOB_NAME",
            "kiwitcms-build",
            "TRAVIS_PULL_REQUEST_SHA",
            "edfd072fd323ea717337407aeb7134c9e8884368",
        ),
        ("JOB_NAME", "kiwitcms-build", "GIT_COMMIT", "edfd072fd323ea717337407aeb7134c9e8884368"),
    ),
    ids=["default", "travis", "jenkins", "git"],
)
@pytest.mark.usefixtures("config_file")
def test_create_plan_and_run(
    testdir, monkeypatch, tcms_username, product_key, product, product_version_key, product_version
):
    """Create new TestPlan & TestRun if TCMS_RUN_ID not configured.

    Product & Product version are set with specified fallback rules.
    """
    monkeypatch.delenv("TCMS_PRODUCT")
    monkeypatch.delenv("TCMS_PRODUCT_VERSION")
    monkeypatch.setenv(product_key, product)
    monkeypatch.setenv(product_version_key, product_version)
    testdir.makepyfile(
        f"""
        def test_create_plan_and_run(pytestconfig):
            plugin = pytestconfig.pluginmanager.get_plugin("pytest-kiwitcms")
            assert plugin.product == "{product}"
            assert plugin.product_version == "{product_version}"
            assert plugin.test_plan["name"] == "Automated test plan for {product}"
            assert plugin.test_plan["author"] == "{tcms_username}"
            assert plugin.test_plan["product_id"] == "{product}"
            assert plugin.test_plan["product_version_id"] == "{product_version}"
        """
    )
    result = testdir.runpytest("--kiwitcms", "-v")
    result.stdout.fnmatch_lines(["*::test_create_plan_and_run PASSED*"])

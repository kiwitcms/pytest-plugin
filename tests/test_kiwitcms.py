# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
import pytest


DEFAULT_CONFIG = (
    ("TCMS_API_URL", "http://another.com"),
    ("TCMS_USERNAME", "user"),
    ("TCMS_PASSWORD", "random"),
)


@pytest.mark.usefixtures("config_file")
def test_file_configuration(testdir):
    """Load configuration from ~/.tcms.conf."""
    testdir.makepyfile(
        """
        def test_file_configuration(pytestconfig):
            plugin = pytestconfig.pluginmanager.get_plugin("pytest-kiwitcms")
            assert plugin.api_url == "http://example.com"
            assert plugin.username == "admin"
            assert plugin.password == "secret"
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
            assert plugin.api_url == "http://another.com"
            assert plugin.username == "user"
            assert plugin.password == "random"
        """
    )
    result = testdir.runpytest("--kiwitcms", "-v")
    result.stdout.fnmatch_lines(["*::test_env_configuration PASSED*"])
    assert result.ret == 0


@pytest.mark.parametrize("envvar, value", DEFAULT_CONFIG)
@pytest.mark.usefixtures("config_file")
def test_config_file_precedence(testdir, monkeypatch, envvar, value):
    """Values from ~/.tcms.conf have higher priority than env variables."""
    monkeypatch.setenv(envvar, value)
    testdir.makepyfile(
        """
        def test_config_file_precedence(pytestconfig):
            plugin = pytestconfig.pluginmanager.get_plugin("pytest-kiwitcms")
            assert plugin.api_url == "http://example.com"
            assert plugin.username == "admin"
            assert plugin.password == "secret"
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
            plugin = pytestconfig.pluginmanager.get_plugin("kiwitcms")
        """
    )
    result = testdir.runpytest("--kiwitcms", "-v")
    result.stderr.fnmatch_lines(["Exit: Option api_url is empty"])
    assert result.ret == 1


def test_kiwitcms_pytest(testdir):
    testdir.makepyfile(
        """
        import pytest
        def test_pass():
            assert 1 == 1
        def test_fail():
            assert 1 == 2
        @pytest.mark.skip()
        def test_skip():
            assert 1 == 1
        def test_error(test):
            assert 1 == ""
        """
    )
    testdir.runpytest("--kiwitcms")

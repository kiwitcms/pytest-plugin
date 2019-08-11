# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
import os

import pytest

pytest_plugins = "pytester"  # pylint: disable=invalid-name

DEFAULT_API_URL = "https://demo.kiwitcms.org/xml-rpc/"
DEFAULT_USERNAME = "PytestTest"
DEFAULT_PASSWORD = "random"

# Valid values for demo.kiwitcms.org
DEFAULT_PRODUCT = "31"
DEFAULT_PRODUCT_VERSION = "721"


@pytest.fixture(scope="session")
def tcms_api_url():
    return os.environ.get("TCMS_API_URL", DEFAULT_API_URL)


@pytest.fixture(scope="session")
def tcms_username():
    return os.environ.get("TCMS_USERNAME", DEFAULT_USERNAME)


@pytest.fixture(scope="session")
def tcms_password():
    return os.environ.get("TCMS_PASSWORD", DEFAULT_PASSWORD)


@pytest.fixture()
def config_content(tcms_api_url, tcms_username, tcms_password):
    return f"""
[tcms]
url = {tcms_api_url}
username = {tcms_username}
password = {tcms_password}"""


@pytest.fixture
def config_file(tmp_path, monkeypatch, config_content):
    """Temporarily create ~/.tcms.conf with example config."""
    monkeypatch.setenv("HOME", str(tmp_path))
    config = tmp_path / ".tcms.conf"
    config.write_text(config_content)


@pytest.fixture(autouse=True)
def environ_config(monkeypatch):
    """Global setup for values required for TestPlan & TestRun.

    Could be changed in tests."""
    monkeypatch.setenv("TCMS_PRODUCT", DEFAULT_PRODUCT)
    monkeypatch.setenv("TCMS_PRODUCT_VERSION", DEFAULT_PRODUCT_VERSION)


def replace_password(password):
    def replace(request):
        request._body = request._body.replace(
            password.encode("utf8"), DEFAULT_PASSWORD.encode("utf8")
        )
        return request

    return replace


@pytest.fixture(scope="session")
def vcr_config(tcms_password):
    return {
        "decode_compressed_response": True,
        "before_record_request": replace_password(tcms_password),
    }

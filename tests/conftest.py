# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
import pytest

pytest_plugins = ["pytester"]  # pylint: disable=invalid-name


DEFAULT_CONFIG_CONTENT = """
[tcms]
url = http://example.com
username = admin
password = secret"""


@pytest.fixture
def config_file(tmp_path, monkeypatch):
    """Temporarily create ~/.tcms.conf with example config."""
    monkeypatch.setenv("HOME", str(tmp_path))
    config = tmp_path / ".tcms.conf"
    config.write_text(DEFAULT_CONFIG_CONTENT)

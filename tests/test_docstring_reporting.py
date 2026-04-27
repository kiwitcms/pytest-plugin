# -*- coding: utf-8 -*-
# Copyright (c) 2026 Carlos Martinez <jcmartinez2129@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
#
# pylint: disable=redefined-outer-name

from unittest.mock import MagicMock, patch

import pytest

from tcms_pytest_plugin import Backend, KiwiTCMSPlugin


@pytest.fixture
def plugin():
    with patch("tcms_pytest_plugin.Backend") as mock_backend_cls:
        instance = MagicMock()
        instance.plan_id = 1
        instance.run_id = 1
        instance.test_case_get_or_create.return_value = ({"id": 99, "text": None}, True)
        instance.add_test_case_to_run.return_value = [{"id": 42}]
        mock_backend_cls.return_value = instance

        p = KiwiTCMSPlugin()
        p.backend = instance
        yield p


def _make_item(nodeid, docstring):
    """Create a minimal mock pytest item with a function docstring."""
    item = MagicMock()
    item.nodeid = nodeid
    item.function.__doc__ = docstring
    return item


def _simulate_collection(plugin, items):
    session = MagicMock()
    session.items = items
    plugin.pytest_collection_finish(session)


def _simulate_logstart(plugin, nodeid):
    plugin.pytest_runtest_logstart(nodeid=nodeid, location=("", 0, ""))


def test_docstring_is_sent_as_test_case_text(plugin):
    """Test case body must be set from the function docstring when present."""
    items = [
        _make_item(
            "tests/test_foo.py::test_intent", "Verify the widget resets on power-up."
        )
    ]
    _simulate_collection(plugin, items)
    _simulate_logstart(plugin, "tests/test_foo.py::test_intent")

    plugin.backend.update_test_case_text.assert_called_once_with(
        99, "Verify the widget resets on power-up."
    )


def test_no_update_when_docstring_is_absent(plugin):
    """update_test_case_text must not be called when the test has no docstring."""
    item = MagicMock()
    item.nodeid = "tests/test_foo.py::test_no_doc"
    item.function.__doc__ = None
    _simulate_collection(plugin, [item])
    _simulate_logstart(plugin, "tests/test_foo.py::test_no_doc")

    plugin.backend.update_test_case_text.assert_not_called()


def test_no_update_when_docstring_is_empty_string(plugin):
    """update_test_case_text must not be called when the docstring is an empty string."""
    items = [_make_item("tests/test_foo.py::test_empty_doc", "")]
    _simulate_collection(plugin, items)
    _simulate_logstart(plugin, "tests/test_foo.py::test_empty_doc")

    plugin.backend.update_test_case_text.assert_not_called()


def test_multiline_docstring_is_cleandoc_normalised(plugin):
    """inspect.cleandoc must be used so internal indentation is normalised."""
    raw_doc = (
        "\n    Verify the widget resets on power-up."
        "\n\n    Precondition: widget is powered.\n    "
    )
    items = [_make_item("tests/test_foo.py::test_multiline", raw_doc)]
    _simulate_collection(plugin, items)
    _simulate_logstart(plugin, "tests/test_foo.py::test_multiline")

    expected = (
        "Verify the widget resets on power-up.\n\nPrecondition: widget is powered."
    )
    plugin.backend.update_test_case_text.assert_called_once_with(99, expected)


def test_item_without_function_attribute_is_skipped(plugin):
    """Items without a .function attribute (e.g. doctest items) must not crash collection."""
    item = MagicMock(spec=[])  # no attributes at all
    item.nodeid = "tests/test_foo.py::test_synthetic"
    session = MagicMock()
    session.items = [item]

    plugin.pytest_collection_finish(session)  # must not raise

    plugin.backend.update_test_case_text.assert_not_called()


def test_docstring_not_sent_for_different_nodeid(plugin):
    """Docstring for test_a must be sent when test_a runs, but not when test_b runs."""
    item_a = _make_item("tests/test_foo.py::test_a", "Intention A")
    item_b = _make_item("tests/test_foo.py::test_b", None)
    _simulate_collection(plugin, [item_a, item_b])

    _simulate_logstart(plugin, "tests/test_foo.py::test_a")
    plugin.backend.update_test_case_text.assert_called_once_with(99, "Intention A")

    plugin.backend.update_test_case_text.reset_mock()

    _simulate_logstart(plugin, "tests/test_foo.py::test_b")
    plugin.backend.update_test_case_text.assert_not_called()


def test_backend_update_test_case_text_calls_rpc():
    """Backend.update_test_case_text must call TestCase.update with the text field."""
    backend = Backend.__new__(Backend)
    backend.rpc = MagicMock()

    backend.update_test_case_text(test_case_id=7, text="Some intention.")

    backend.rpc.TestCase.update.assert_called_once_with(7, {"text": "Some intention."})

# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Copyright (c) 2022 Alexander Todorov <atodorov@otb.bg>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
#
# pylint: disable=comparison-of-constants, unused-argument
import pytest


def test_should_pass_when_assertion_passes():
    assert True


def test_should_fail_when_assertion_fails():
    assert 1 == 2


@pytest.mark.skip("We've decided not to test this")
def test_should_skip_if_marked_as_such():
    assert True


def test_should_error_with_non_existing_fixture(non_existing):
    assert 1 == ""

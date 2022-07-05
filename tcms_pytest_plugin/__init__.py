# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Copyright (c) 2021 Bryan Mutai <mutaiwork@gmail.com>
# Copyright (c) 2021-2022 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
#
# pylint: disable=unused-argument, no-self-use


import pytest
from tcms_api import plugin_helpers

from .version import __version__


def pytest_addoption(parser):
    group = parser.getgroup("kiwitcms")
    group.addoption(
        "--kiwitcms",
        action="store_true",
        help="Enable recording of test results in Kiwi TCMS.",
    )


def pytest_configure(config):
    if config.getoption("--kiwitcms"):
        config.pluginmanager.register(
            KiwiTCMSPlugin(config.getoption("--verbose")),
            name="kiwitcms",
        )


class Backend(plugin_helpers.Backend):
    name = "kiwitcms-pytest-plugin"
    version = __version__


class KiwiTCMSPlugin:
    executions = []
    status_id = 0
    status_weight = 0
    comment = ""

    def __init__(self, verbose=False):
        self.backend = Backend(prefix="[pytest]", verbose=verbose)

    def pytest_runtestloop(self, session):
        self.backend.configure()

    def pytest_runtest_logstart(self, nodeid, location):
        self.status_weight = 0
        self.comment = ""

        test_case, _ = self.backend.test_case_get_or_create(nodeid)
        self.backend.add_test_case_to_plan(test_case["id"], self.backend.plan_id)
        self.executions = self.backend.add_test_case_to_run(
            test_case["id"], self.backend.run_id
        )

    @pytest.hookimpl(hookwrapper=True)
    def pytest_report_teststatus(self, report, config):
        yield

        # this hooks is executed 3 times for setup/call/teardown each of which
        # has their own status. Thus a positive status cannot override a negative one
        # Positive statuses are considered only in the beginning
        if report.when in ["setup", "call"]:
            if self.status_weight >= 0 and report.outcome == "passed":
                self.status_id = self.backend.get_status_id("PASSED")
                self.status_weight = 1
            elif self.status_weight >= 0 and report.outcome == "skipped":
                self.status_id = self.backend.get_status_id("WAIVED")
                self.status_weight = 1

        # a negative status is stronger, will always override any other status
        # negative statuses are considered in every occasion
        if report.outcome in ["error", "failed"]:
            self.status_id = self.backend.get_status_id(report.outcome.upper())
            self.status_weight = -1
            self.comment = f"<pre>\n{report.longrepr}\n</pre>"

    def pytest_runtest_logfinish(self, nodeid, location):
        for execution in self.executions:
            self.backend.update_test_execution(
                execution["id"], self.status_id, self.comment
            )

    @pytest.hookimpl(hookwrapper=True)
    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        yield
        self.backend.finish_test_run()

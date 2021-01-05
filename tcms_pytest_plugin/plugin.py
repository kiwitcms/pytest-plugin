# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
# pylint: disable=unused-argument, no-self-use


import pytest
from tcms_api.plugin_helpers import Backend

DEFAULT_CONFIG_PATH = "~/.tcms.conf"

backend = Backend(prefix='[pytest]')


def pytest_addoption(parser):
    group = parser.getgroup("kiwitcms")
    group.addoption(
        "--kiwitcms", action="store_true", help="Enable recording of test results in Kiwi TCMS."
    )


def pytest_configure(config):
    if config.getoption("--kiwitcms"):
        config.pluginmanager.register(
            KiwiTCMSPlugin(),
            name="pytest-kiwitcms",
        )


class KiwiTCMSPlugin:
    test_execution_id = 0
    status_id = 0
    comment = ''

    def pytest_runtestloop(self, session):
        backend.configure()

    def pytest_runtest_logstart(self, nodeid, location):
        test_case, _ = backend.test_case_get_or_create(nodeid)
        backend.add_test_case_to_plan(test_case['id'], backend.plan_id)
        self.test_execution_id = backend.add_test_case_to_run(test_case['id'], backend.run_id)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_report_teststatus(self, report, config):
        yield
        if report.when == 'teardown':
            if report.outcome == 'passed':
                self.status_id = backend.get_status_id('PASSED')
            elif report.outcome == 'failed':
                self.status_id = backend.get_status_id('FAILED')
            elif report.outcome == 'skipped':
                self.status_id = backend.get_status_id('WAIVED')

    def pytest_runtest_logfinish(self, nodeid, location):
        backend.update_test_execution(self.test_execution_id, self.status_id, self.comment)

    @pytest.hookimpl(hookwrapper=True)
    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        yield
        backend.finish_test_run()

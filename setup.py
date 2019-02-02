#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
from setuptools import setup
import tcms_pytest_plugin

README = open("README.rst").read()
REQUIREMENTS = open("requirements.txt").readlines()

setup(
    name="kiwitcms-pytest-plugin",
    version=tcms_pytest_plugin.__version__,
    author="Dmitry Dygalo",
    author_email="dadygalo@gmail.com",
    maintainer="Kiwi TCMS",
    maintainer_email="info@kiwitcms.org",
    url="https://github.com/kiwitcms/pytest-plugin",
    description="Pytest plugin for Kiwi TCMS test case management system",
    long_description=README,
    packages=["tcms_pytest_plugin"],
    python_requires=">=3.6",
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    entry_points={"pytest11": ["tcms_pytest_plugin = tcms_pytest_plugin.plugin"]},
)

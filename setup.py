#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 Dmitry Dygalo <dadygalo@gmail.com>
# Copyright (c) 2021 Bryan Mutai <mutaiwork@gmail.com>
# Copyright (c) 2021-2022 Alexander Todorov <atodorov@otb.bg>
#
# Licensed under the GPLv3: https://www.gnu.org/licenses/gpl.html
import os
from setuptools import setup


def get_version():
    version_py_path = os.path.join("tcms_pytest_plugin", "version.py")
    with open(version_py_path, encoding="utf-8") as version_file:
        version = version_file.read()
        return (
            version.replace(" ", "")
            .replace("__version__=", "")
            .strip()
            .strip("'")
            .strip('"')
        )


with open("README.rst", encoding="utf-8") as readme:
    README = readme.read()

with open("requirements.txt", encoding="utf-8") as requirements:
    REQUIREMENTS = requirements.readlines()

setup(
    name="kiwitcms-pytest-plugin",
    version=get_version(),
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    entry_points={"pytest11": ["tcms_pytest_plugin = tcms_pytest_plugin"]},
)

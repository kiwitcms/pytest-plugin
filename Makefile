.PHONY: doc8
doc8:
	doc8 README.rst

.PHONY: flake8
flake8:
	@flake8 --exclude=.git *.py tcms_pytest_plugin tests

.PHONY: pylint
pylint:
	pylint -d missing-docstring tcms_pytest_plugin/ tests/

.PHONY: test
test:
	pytest --kiwitcms

.PHONY: check-build
check-build:
	./tests/bin/check-build

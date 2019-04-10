BUILD_DIR := build
COVERAGE_DIR := ./code_coverage
COVERAGE_FILE := .coverage
DIST_DIR := dist
EGG_DIR := f5_cloud_cli.egg-info
PACKAGE_DIR := f5cloudcli
TEST_DIR := tests

build:
	echo "Creating package artifacts"
	python3 setup.py sdist bdist_wheel
unit_test:
	echo "Running unit tests (incl code coverage)";
	pytest --cov=${PACKAGE_DIR} ${TEST_DIR}/;
lint:
	echo "Running linter (any error will result in non-zero exit code)";
	pylint ${PACKAGE_DIR}/;
coverage: unit_test
	echo "Generating code coverage documentation"
	coverage html
clean:
	echo "Removing artifacts"
	rm -rf ${BUILD_DIR}
	rm -rf ${DIST_DIR}
	rm -rf ${EGG_DIR}
	rm -rf ${COVERAGE_DIR}
	rm -rf ${COVERAGE_FILE}
.PHONY: clean

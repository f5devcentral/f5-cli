BUILD_DIR := build
CODE_DOCS_DIR := ./code_docs
COVERAGE_DIR := ./code_coverage
COVERAGE_FILE := .coverage
DIST_DIR := dist
EGG_DIR := f5_cloud_cli.egg-info
PACKAGE_DIR := f5cloudcli
TEST_DIR := tests
UNIT_TEST_DIR := ${TEST_DIR}/unittests

# Sphinx variables for building docs
SPHINXOPTS    = 
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = docs/_build

# Sphinx Internal variables
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) ./docs

build:
	echo "Creating package artifacts"
	python3 setup.py sdist bdist_wheel
unit_test:
	echo "Running unit tests (incl code coverage)";
	pytest --flake8 --cov=${PACKAGE_DIR} ${UNIT_TEST_DIR}/;
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
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
	cp -R docs/_build ${CODE_DOCS_DIR}
.PHONY: clean

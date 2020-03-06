BUILD_DIR := build
CODE_DOCS_DIR := ./code_docs
COVERAGE_DIR := ./code_coverage
COVERAGE_FILE := .coverage
DIST_DIR := dist
EGG_DIR := f5_cli.egg-info
PACKAGE_DIR := f5cli
TEST_DIR := tests
UNIT_TEST_DIR := ${TEST_DIR}/unittests

# Sphinx variables for building docs
SPHINXOPTS    = 
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = docs/_build
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) ./docs

build:
	echo "Creating package artifacts"
	python3 setup.py sdist bdist_wheel
unit_test:
	echo "Running unit tests (incl code coverage)";
	pytest --cov=${PACKAGE_DIR} -vv ${UNIT_TEST_DIR}/;
lint:
	echo "Running linter (any error will result in non-zero exit code)";
	flake8 ${PACKAGE_DIR}/ ${TEST_DIR}/;
	pylint -j 0 ${PACKAGE_DIR}/ ${TEST_DIR}/;
coverage: unit_test
	echo "Generating code coverage documentation"
	coverage html
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
code_docs: html
	cp -R ${BUILDDIR}/ ${CODE_DOCS_DIR}
	@echo "Docs finished. The are located in $(CODE_DOCS_DIR)"
upload: build
	echo "Uploading package to PyPI";
	# set username/password using TWINE_USERNAME/TWINE_PASSWORD
	# or using keyring for automated scenarios
	twine check ${DIST_DIR}/*
	twine upload --skip-existing ${DIST_DIR}/*
clean:
	echo "Removing artifacts"
	rm -rf ${BUILD_DIR}
	rm -rf ${CODE_DOCS_DIR}
	rm -rf ${DIST_DIR}
	rm -rf ${EGG_DIR}
	rm -rf ${COVERAGE_DIR}
	rm -rf ${COVERAGE_FILE}
	find . -type d -name __pycache__ -exec rm -r {} \+
.PHONY: clean

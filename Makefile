TEST_DIR := tests

unit_test:
	echo "Running unit tests"; \
	pytest ${TEST_DIR}/
clean:
	echo "Removing artifacts..."
.PHONY: clean

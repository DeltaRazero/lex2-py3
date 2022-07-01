
# Select Python testing framework, based on availability
ifneq ($(shell which pytest),)
    TEST_FRAMEWORK = pytest
endif
TEST_FRAMEWORK ?= python -m unittest

# *****************************************************************************

.PHONY: all build install test upload docs
all: build install

build:
	# Clean dist folder (if it exists)
	find ./ -type d -name "dist" -exec rm -r {} \; -prune

	# Create source archive and wheel
	python setup.py sdist bdist_wheel

	# Clean after building
	python setup.py clean --all
	find ./ -type d -name "*.egg-info" -exec rm -r {} \; -prune

test:
	$(TEST_FRAMEWORK) tests

install:
	python setup.py install

docs:
	cd docs && $(MAKE)

upload:
	python -m twine upload dist/*

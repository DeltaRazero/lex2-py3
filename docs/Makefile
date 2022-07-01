
.PHONY: all build diagrams
all: diagrams build

DOC_ROOT = $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

# *****************************************************************************
#   Sphinx
# *****************************************************************************

SPHINXOPTS  ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR    = src
BUILDDIR     = build

# Put it first so that "make" without argument is like "make help".
# help:
# 	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
build: diagrams
	rm -rf src/_autosummary
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O) -E -a

clean:
	rm -rf build

# *****************************************************************************
#   PlantUML
# *****************************************************************************

diagrams:
	cd src/diagrams && $(MAKE) png

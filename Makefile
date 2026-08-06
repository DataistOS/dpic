# Minimal makefile for Sphinx documentation
#

SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile build-all build-all-log build-multiversion

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Target to clean and build HTML, EPUB, and PDF formats
build-all:
	@echo "=================================================="
	@echo "Running plan.rst to plan.json sync script..."
	@echo "=================================================="
	python3 _script/rst_to_json.py

	@echo "=================================================="
	@echo "Cleaning previous builds..."
	@echo "=================================================="
	rm -rf _build/*

	@echo "=================================================="
	@echo "Generating HTML website..."
	@echo "=================================================="
	sphinx-build -b html . _build/html

	@echo "=================================================="
	@echo "Generating EPUB ebook..."
	@echo "=================================================="
	sphinx-build -b epub . _build/epub

	@echo "=================================================="
	@echo "Generating PDF documentation..."
	@echo "=================================================="
	sphinx-build -b latex . _build/latex
	@echo "Compiling LaTeX to PDF via xelatex (Pass 1)..."
	cd _build/latex && xelatex -interaction=nonstopmode *.tex
	@echo "Re-compiling LaTeX to finalize cross-references (Pass 2)..."
	cd _build/latex && xelatex -interaction=nonstopmode *.tex

	@echo "=================================================="
	@echo "ALL BUILDS COMPLETED SUCCESSFULLY!"
	@echo "=================================================="

# Target to run build-all and save timestamped logs into _templates directory
build-all-log:
	@mkdir -p _templates
	@$(MAKE) build-all 2>&1 | tee "_templates/logs/$$(date +'%Y%m%d%H%M%S')_build_logs.txt"

build-multiversion:
	@echo "=================================================="
	@echo "Running plan.rst to plan.json sync script..."
	@echo "=================================================="
	python3 _script/rst_to_json.py
	@echo "=================================================="
	@echo "Cleaning previous multiversion HTML build..."
	@echo "=================================================="
	rm -rf _build/html
	@echo "=================================================="
	@echo "Generating Multi-version HTML website via Git..."
	@echo "=================================================="
	sphinx-multiversion . _build/html
	@echo "=================================================="
	@echo "MULTIVERSION HTML BUILD COMPLETED SUCCESSFULLY!"
	@echo "=================================================="

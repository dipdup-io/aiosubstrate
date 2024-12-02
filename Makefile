.PHONY: $(MAKECMDGOALS)
MAKEFLAGS += --no-print-directory
##
##  🚧 aiosubstrate developer tools
##
PACKAGE=aiosubstrate
SOURCE=src tests examples


help:           ## Show this help (default)
	@grep -Fh "##" $(MAKEFILE_LIST) | grep -Fv grep -F | sed -e 's/\\$$//' | sed -e 's/##//'

##
##-- Dependencies
##

install:        ## Install dependencies
	uv sync --extra full --frozen

update:         ## Update dependencies
	uv lock

##
##-- CI
##

all:            ## Run an entire CI pipeline
	make format lint test

format:         ## Format with ruff
	ruff format

lint:           ## Lint with all tools
	make ruff mypy

test:           ## Run tests
	COVERAGE_CORE=sysmon pytest tests

##

ruff:           ## Lint with ruff
	ruff check --fix --unsafe-fixes ${SOURCE}

mypy:           ## Lint with mypy
	mypy ${SOURCE}

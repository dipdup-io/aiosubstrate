.PHONY: $(MAKECMDGOALS)
MAKEFLAGS += --no-print-directory
##
##  🚧 DipDup developer tools
##
PACKAGE=aiosubstrate
TAG=latest
SOURCE=aiosubstrate test examples


help:           ## Show this help (default)
	@grep -Fh "##" $(MAKEFILE_LIST) | grep -Fv grep -F | sed -e 's/\\$$//' | sed -e 's/##//'

##
##-- Dependencies
##

install:        ## Install dependencies
	uv sync --extra full

update:         ## Update dependencies
	uv lock

##
##-- CI
##

all:            ## Run an entire CI pipeline
	make format lint test

format:         ## Format with all tools
	make black

lint:           ## Lint with all tools
	make ruff mypy

test:           ## Run tests
	COVERAGE_CORE=sysmon pytest test

##

black:          ## Format with black
	black ${SOURCE}

ruff:           ## Lint with ruff
	ruff check --fix --unsafe-fixes ${SOURCE}

mypy:           ## Lint with mypy
	mypy ${SOURCE}

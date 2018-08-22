MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

.PHONY: check
check:
	pytest

.PHONY: fmt
fmt:
	isort -rc django_alive
	black django_alive

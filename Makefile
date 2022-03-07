####################
# setup

NAME=earthlib
CONDA=conda run --name ${NAME}
.PHONY: all test clean

# help docs
.DEFAULT: help
help:
	@echo "--- [ $(NAME) developer tools ] --- "
	@echo ""
	@echo "make init - initialize conda dev environment"
	@echo "make test - run package tests"
	@echo "make collections - generate new formatted collections.json file"
	@echo "make pypi - build and upload pypi package"

####################
# utils

init:
	conda env list | grep -q ${NAME} || conda create --name=${NAME} python=3.7 -y
	${CONDA} conda install -c conda-forge mamba -y
	${CONDA} mamba install --file environment.yml -c conda-forge -y
	${CONDA} pip install -e .
	${CONDA} pip install -r requirements-dev.txt
	${CONDA} mamba install pre-commit -c conda-forge
	${CONDA} pre-commit install

test:
	${CONDA} pytest --cov --no-cov-on-fail --cov-report=term-missing:skip-covered

collections:
	${CONDA} python scripts/generate_collections.py

pypi:
	rm -rf dist/
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

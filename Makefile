####################
# setup

NAME=earthlib
<<<<<<< HEAD
CONDA=conda run --no-capture-output --name ${NAME}
.PHONY: init docs test collections pypi
=======
CONDA=conda run --name ${NAME}
.PHONY: all test clean
>>>>>>> truncated history

# help docs
.DEFAULT: help
help:
	@echo "--- [ $(NAME) developer tools ] --- "
	@echo ""
	@echo "make init - initialize conda dev environment"
<<<<<<< HEAD
	@echo "make docs - install mkdocs dependencies"
=======
>>>>>>> truncated history
	@echo "make test - run package tests"
	@echo "make collections - generate new formatted collections.json file"
	@echo "make pypi - build and upload pypi package"

####################
# utils

init:
	conda env list | grep -q ${NAME} || conda create --name=${NAME} python=3.7 -y
<<<<<<< HEAD
	${CONDA} pip install -e .
	${CONDA} pip install pre-commit pytest pytest-cov pytest-xdist twine
	${CONDA} pre-commit install

docs:
	${CONDA} pip install mkdocs mkdocs-material mkdocstrings[python] mkdocs-jupyter livereload

test:
	${CONDA} pytest -n auto --cov --no-cov-on-fail --cov-report=term-missing:skip-covered
=======
	${CONDA} conda install -c conda-forge mamba -y
	${CONDA} mamba install --file environment.yml -c conda-forge -y
	${CONDA} pip install -e .
	${CONDA} pip install -r requirements-dev.txt
	${CONDA} mamba install pre-commit -c conda-forge
	${CONDA} pre-commit install

test:
	${CONDA} pytest --cov --no-cov-on-fail --cov-report=term-missing:skip-covered
>>>>>>> truncated history

collections:
	${CONDA} python scripts/generate_collections.py

pypi:
	rm -rf dist/
	python3 setup.py sdist bdist_wheel
	twine upload dist/*

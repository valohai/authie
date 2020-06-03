# laituri — Docker Toolkit for Python

[![Build Status](https://travis-ci.com/valohai/laituri.svg?branch=master)](https://travis-ci.com/valohai/laituri)
[![codecov](https://codecov.io/gh/valohai/laituri/branch/master/graph/badge.svg)](https://codecov.io/gh/valohai/laituri)

`laituri` is a set of Docker-related Python snippets used at [Valohai](https://valohai.com/).

## Development

Installing editable library version in the current virtual environment.

```bash
pip install -e .[dev]   # optionally replace . with the path to laituri source root
isort -y                # automatically enforce import style rules
flake8                  # run code style checker
pydocstyle              # run documentation style checker
pytest --cov            # run unit tests and print test coverage

python
>>> import laituri; print(laituri.__version__)
```

## Making a Release

Pump the version number accordingly in `laituri/__init__.py` and then...

```bash
# `pip install twine` if you don't have it (PyPI project uploader)
# NOTE: the following will delete everything except `.idea/` in source directory but not tracked by git!
git clean -fdx -e .idea/
python setup.py sdist bdist_wheel
twine upload dist/*

# and update git remote
git add .
git commit -m "Pump to v0.2"
git push
```

# authie — Authentication Toolkit for Python

`authie` is a set of authentication-related Python snippets used at [Valohai](https://valohai.com/).

## Development

Installing editable library version in the current virtual environment.

```bash
pip install -e .[dev]   # optionally replace . with the path to authie source root
pytest --cov            # run unit tests and print test coverage
flake8                  # run code style checker
pydocstyle              # run documentation style checker
isort -y                # automatically enforce import style rules

python
>>> import authie; print(authie.__version__)
```

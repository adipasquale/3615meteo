# 3615meteo

simple text interface to meteofrance marine data

## Dev

`poetry run jupyter lab`

`poetry run livereload`

## Tests

`python -m tests.test_parse_bulletin_cote_xml`

## Local setup

You need pyenv, pyenv-virtualenv and poetry

```
pyenv install `cat .python-version`
pyenv virtualenv adipasquale.github.com `cat .python-version`
cd scraper
poetry install
```

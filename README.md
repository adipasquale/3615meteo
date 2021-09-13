# 3615meteo

![3615 Météo](https://raw.githubusercontent.com/adipasquale/3615meteo/main/static_assets/logo.png)

La météo marine de Météo France en version minimaliste, que du texte, chargement instantané, lisible sur mobile

## Fonctionnement

Un 

## Développement

Installez pyenv, pyenv-virtualenv et poetry

```sh
pyenv install 3.9.7
poetry install
```

Le script principal pour scraper, parser et générer les fichiers HTML est celui-ci :

```sh
poetry run python lib/build.py
```

Il y a aussi un serveur de développement qui relancera la compilation à chaque changement de fichier, et rafraîchira automatiquement le navigateur : 

`poetry run livereload`


Il y a quelques notebooks jupyter pour tester le scraping et le parsing

`poetry run jupyter lab`

## Tests

`python -m tests.test_parse_bulletin_cote_xml`


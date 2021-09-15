# 3615 Météo

![3615 Météo](https://raw.githubusercontent.com/adipasquale/3615meteo/main/static_assets/logo.png)

La météo marine de Météo France en version minimaliste, que du texte, chargement instantané, lisible sur mobile

## Fonctionnement

Les bulletins météo marin côtiers réguliers (BMRCOTE) et spéciaux (BMSCOTE) de Météo France sont publiés trois fois par jour vers 06h30, 12h30 et 18h30.

Une GitHub Action est programmée pour s'éxecuter à ces heures-ci. Elle déclenche un script Python qui :

- récupère les fichiers JSON de bulletins spéciaux le cas échéant
- récupère les fichiers XML de bulletins réguliers
- génère des fichiers HTML pour chacun des bulletins + un index
- committe ces fichiers dans le répértoire `/docs` de ce repo

Le site est alors disponible via l'hébergement de GitHub Pages à l'adresse [adipasquale.github.io/3615meteo](https://adipasquale.github.io/3615meteo)

## Développement

Installez pyenv et poetry

```sh
pyenv install 3.9.7
poetry install
```

Le script principal pour scraper, parser et générer les fichiers HTML est celui-ci :

```sh
poetry run python -m meteo.scripts.build
```

Il y a aussi un serveur de développement qui relancera la compilation à chaque changement de fichier, et rafraîchira automatiquement le navigateur :

```sh
poetry run python -m meteo.scripts.local_server
```

Il y a aussi quelques notebooks jupyter pour tester le scraping et le parsing

```sh
poetry run jupyter lab
```

## Tests

```sh
poetry run python -m meteo.tests.test_parse_bulletin_cote_xml
poetry run python -m meteo.tests.test_parse_bulletin_special_json
```

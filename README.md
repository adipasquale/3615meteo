# 3615 Météo

![3615 Météo](https://raw.githubusercontent.com/adipasquale/3615meteo/main/static_assets/logo.png)

[voir sur 3615meteo.live](https://www.3615meteo.live)

La météo marine de Météo France en version légère et lisible

<img width="1099" alt="Screenshot 2021-09-17 at 10 46 50" src="https://user-images.githubusercontent.com/883348/133753567-f9eb5b00-7c21-4912-89d5-82a043406474.png">

## Fonctionnement

Les bulletins météo marin côtiers réguliers (BMRCOTE) et spéciaux (BMSCOTE) de Météo France sont publiés trois fois par jour vers 06h30, 12h30 et 18h30.

Une GitHub Action est programmée pour s'éxecuter à ces heures-ci. Elle déclenche un script Python qui :

- récupère les fichiers JSON de bulletins spéciaux le cas échéant
- récupère les fichiers XML de bulletins réguliers
- génère des fichiers JSON d'API pour chacun des bulletins et un index par type de bulletin
- génère des fichiers HTML pour chacun des bulletins + un index
- committe ces fichiers dans le répértoire `/docs` de ce repo

Le site est alors disponible via l'hébergement de GitHub Pages à l'adresse [3615meteo.live](https://www.3615meteo.live)

## API

Une API de fichiers statiques est disponibles aux routes suivantes:

- [3615meteo.live/api/bulletins_cotiers.json](https://3615meteo.live/api/bulletins_cotiers.json)
- [3615meteo.live/api/bulletins_cotiers/`CODE_BULLETIN`.json](https://3615meteo.live/api/bulletins_cotiers.json)
- [3615meteo.live/api/bulletins_speciaux.json](https://3615meteo.live/api/bulletins_speciaux.json)
- [3615meteo.live/api/bulletins_speciaux/`CODE_BULLETIN`.json](https://3615meteo.live/api/bulletins_speciaux.json)

où `CODE_BULLETIN` est au format `BMSCOTE-02` ou `BMRCOTE-02-02`

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
poetry run python -m unittest discover meteo/tests
```

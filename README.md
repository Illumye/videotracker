# VideoTracker_G4

[![Videotracker Tests](https://github.com/Illumye/videotracker/actions/workflows/python-app.yml/badge.svg)](https://github.com/Illumye/videotracker/actions/workflows/python-app.yml)

## Sommaire

- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Licence](#licence)
- [TODO's](#todos)

## Description

Ce projet est un outil de tracking de vidéos. Il permet de suivre les mouvements d'un objet dans une vidéo.

## Requirements

- Python 3.6 ou plus
- OpenCV
- Numpy
- Matplotlib
- Tkinter

## Installation

Pour initialiser un environnement virtuel (si non-existant) et installer les dépendances, exécutez le script `install_deps.sh` :

```bash
$ ./src/install_deps.sh
```

## Utilisation


```bash
$ python3 src/application.py
```

ou

```bash
$ chmod +x src/application.py
$ ./src/application.py
```

## Licence

Ce projet est sous licence MIT.

## TODO's

- [x] Supprimer les fichiers `.create` dans chaque dossier vide
- [ ] Issue #1
    - [x] Task #7 (self.points dans le contrôleur -> modèle)
    - [x] Task #8 (self.origin dans le contrôleur -> modèle)
    - [x] Task #9 (Réaffichage du tableau lorsque l'utilisateur le demande)
    - [ ] Task #10 (Mise à jour de la fenêtre du tableau des points lors de l'ouverture )
- [x] Issue #2 (Tests)
    - [x] Test : FileRepo
    - [x] Test : Point
    - [x] Test : VideoController

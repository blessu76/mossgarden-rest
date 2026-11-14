---
title: "Pourquoi nous gardons deux copies de la sauvegarde"
description: "Perdre un jardin que l'on a fait pousser est le pire, alors la sauvegarde est répartie entre un fichier principal et une copie de secours."
copy_review: iris 2026-11-14
---
Moss Garden, un jeu idle pour iOS, protège votre jardin avec deux garde-fous : une somme de contrôle qui détecte une sauvegarde endommagée et une copie de secours distincte à partir de laquelle il restaure, en vous prévenant. Reculer l'horloge de l'appareil pour récupérer des récompenses est également détecté, et cette période n'est pas comptabilisée.

## Deux garde-fous pour la sauvegarde

Dans un jeu idle, le plus décourageant est de perdre le jardin qu'on a fait grandir. La sauvegarde a donc deux garde-fous.

Le premier est une somme de contrôle : une valeur de vérification est écrite avec la sauvegarde, et si elle ne correspond pas au chargement, le fichier est considéré comme endommagé. Le second est la copie de secours : le fichier principal et la copie sont conservés séparément, si bien que si le principal se corrompt, nous restaurons depuis la copie et nous vous le disons. Nous avons aussi veillé à l'ordre des opérations, pour qu'un fichier principal corrompu n'écrase jamais une copie saine.

## Retours en arrière de l'horloge

Il fallait aussi empêcher l'astuce qui consiste à reculer l'horloge de l'appareil pour récupérer des récompenses. Quand un retour en arrière de l'horloge est détecté, cette période n'est pas comptabilisée, et l'appli vous en informe.

## Garder les anciennes sauvegardes utilisables

Quand nous ajoutons des fonctionnalités, nous conservons le format de sauvegarde et n'ajoutons que de nouveaux champs, afin que les anciennes sauvegardes s'ouvrent encore dans les versions plus récentes.

## FAQ

### Que se passe-t-il si le fichier de sauvegarde de Moss Garden est corrompu ?
La somme de contrôle repère l'écart, le jeu restaure la copie de secours distincte et vous indique qu'il l'a fait.

### Puis-je obtenir des récompenses en changeant l'horloge de l'appareil ?
Non. Quand un retour en arrière de l'horloge est détecté, cette période n'est pas comptabilisée, et l'appli vous en informe.

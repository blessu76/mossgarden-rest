---
title: "Comment le premier build TestFlight a été mis en ligne"
description: "Une fois le MVP terminé, le premier build interne est parti, mais le script de déploiement nous a arrêtés une fois en chemin."
copy_review: iris 2026-11-14
---
Le premier MVP de Moss Garden, un jeu idle pour iOS, a été envoyé sur TestFlight en version 1.0.0 (1) pour des tests internes, après qu'un script de déploiement a stoppé la première tentative. Le traitement a pris environ trois minutes, et le build n'a été ni soumis à la validation ni ouvert à des testeurs externes.

## Ce que contenait le MVP

Le premier MVP réunissait huit plantes, le calcul hors ligne, les saisons, un livre de collection, la sauvegarde et les réglages. Nous l'avons ensuite envoyé sur TestFlight en 1.0.0 (1) pour des tests internes. Le traitement a pris environ trois minutes, et nous ne l'avons ni soumis à la validation ni ouvert à des testeurs externes.

## La première tentative a échoué

Quand le script de déploiement a lancé le green gate, une variable d'environnement signifiant « n'incrémente pas le numéro de build » s'est infiltrée dans les tests et les a cassés, et le script s'est arrêté net. Grâce à cet arrêt, aucun mauvais build n'a été envoyé. Nous avons corrigé le problème pour que les processus enfants n'héritent plus de l'environnement extérieur, puis nous avons renvoyé le build.

Déployer peut être pénible, mais nous gardons la règle : si les tests ne sont pas au vert, rien ne part.

## FAQ

### Que contenait le premier build TestFlight de Moss Garden ?
Huit plantes, le calcul hors ligne, les saisons, un livre de collection, la sauvegarde et les réglages, envoyés en 1.0.0 (1) pour des tests internes.

### Moss Garden a-t-il été soumis à la validation de l'App Store ?
Non. Ce build a seulement été envoyé pour des tests internes, et nous ne l'avons pas soumis à la validation.

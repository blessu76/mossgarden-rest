---
title: "Pourquoi afficher la rosée avec des décimales"
description: "La mousse pousse de 0,1 par seconde, mais le compteur de rosée semblait figé. Voici comment nous avons corrigé le format du nombre."
copy_review: iris 2026-11-14
---
Moss Garden est un jeu idle (incrémental) pour iOS, et son compteur de rosée semblait figé parce qu'il n'affichait que des nombres entiers à partir de dix. Nous affichons désormais deux décimales en dessous de 1 et une décimale en dessous de 1 000, et nous arrondissons à l'inférieur pour que le nombre ne promette jamais plus que ce que vous avez.

## Pourquoi le nombre semblait figé

La mousse s'accumulait à 0,1 par seconde, mais le nombre de rosée en haut de l'écran restait identique pendant longtemps. Un testeur nous a dit qu'il ne savait pas si le compteur avançait. La cause était simple : à partir de dix, nous n'affichions que des nombres entiers.

## Ce que nous avons changé

Les valeurs inférieures à 1 affichent maintenant deux décimales, et celles inférieures à 1 000 en affichent une. Les zéros de fin sont supprimés : vous lisez 289 au lieu de 289,0.

La seule vraie décision concernait l'arrondi. Afficher 185,56 comme 185,6 ferait paraître abordable ce que vous ne pouvez pas encore acheter. Nous **arrondissons donc à l'inférieur** : le nombre à l'écran est toujours au plus égal à ce que vous possédez réellement.

C'est un changement minuscule, mais dans un jeu où l'on attend, voir le nombre bouger fait partie de la récompense.

## FAQ

### Pourquoi Moss Garden affiche-t-il la rosée avec des décimales ?
Parce que la mousse pousse de 0,1 par seconde et que les nombres entiers donnaient l'impression que le compteur était figé. Les décimales montrent qu'il avance.

### Le nombre de rosée est-il arrondi à l'inférieur ou au supérieur ?
À l'inférieur. Le nombre à l'écran est toujours au plus égal à la quantité que vous possédez réellement, de sorte que rien ne paraît abordable avant de l'être.

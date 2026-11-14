---
title: "Por qué mostramos el rocío con decimales"
description: "El musgo crece 0,1 por segundo, pero el contador de rocío parecía congelado. Así arreglamos el formato del número."
copy_review: iris 2026-11-14
---
Moss Garden es un juego idle (incremental) para iOS, y su contador de rocío parecía congelado porque a partir de diez solo mostraba números enteros. Ahora mostramos dos decimales por debajo de 1 y un decimal por debajo de 1000, y redondeamos hacia abajo para que el número nunca prometa más de lo que tienes.

## Por qué el número parecía congelado

El musgo se acumulaba a 0,1 por segundo, pero el número de rocío de la parte superior de la pantalla se quedaba igual durante mucho tiempo. Un tester nos dijo que no podía saber si estaba contando siquiera. La causa era simple: a partir de diez solo mostrábamos números enteros.

## Qué cambiamos

Los valores menores que 1 muestran dos decimales y los menores que 1000, uno. Se omiten los ceros finales, así que lees 289 en lugar de 289,0.

La única decisión de verdad fue el redondeo. Mostrar 185,56 como 185,6 haría que algo que aún no puedes comprar pareciera asequible. Por eso **redondeamos hacia abajo**: el número en pantalla es siempre como máximo lo que realmente tienes.

Es un cambio diminuto, pero en un juego sobre esperar, ver moverse el número forma parte de la recompensa.

## Preguntas frecuentes

### ¿Por qué Moss Garden muestra el rocío con decimales?
Porque el musgo crece 0,1 por segundo y, con enteros, el contador parecía congelado. Con decimales se ve que está contando.

### ¿El número de rocío se redondea hacia arriba o hacia abajo?
Hacia abajo. El número en pantalla es siempre como máximo la cantidad que realmente tienes, así que nada parece asequible antes de serlo.

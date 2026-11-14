---
title: "Por qué guardamos dos copias de la partida"
description: "Perder un jardín que has hecho crecer es lo peor, así que el guardado se divide en un archivo principal y una copia de seguridad."
---
Moss Garden, un juego idle para iOS, protege tu jardín con dos salvaguardas: una suma de verificación que detecta un guardado dañado y una copia de seguridad aparte desde la que se restaura, con un aviso. También se detecta que atrases el reloj del dispositivo para cobrar recompensas, y ese tramo no se liquida.

## Dos salvaguardas para el guardado

En un juego idle, lo más molesto es perder el jardín que llevas tiempo cultivando. Por eso el guardado tiene dos salvaguardas.

La primera es una suma de verificación: junto con el guardado se escribe un valor de control, y si al cargar no coincide, el archivo se considera dañado. La segunda es la copia de seguridad: el archivo principal y la copia se guardan por separado, de modo que si el principal se rompe, restauramos desde la copia y te lo decimos. También cuidamos el orden, para que un archivo principal roto nunca sobrescriba una copia sana.

## Retrocesos del reloj

También teníamos que frenar el truco de atrasar el reloj del dispositivo para cobrar recompensas. Cuando se detecta un retroceso del reloj, ese tramo no se liquida y la app te lo comunica.

## Que las partidas antiguas sigan funcionando

Cuando añadimos funciones, mantenemos el formato del guardado y solo agregamos campos nuevos, de modo que las partidas antiguas se abren en versiones más recientes.

## Preguntas frecuentes

### ¿Qué pasa si se rompe el archivo de guardado de Moss Garden?
La suma de verificación detecta la discrepancia, el juego restaura desde la copia de seguridad aparte y te avisa de que lo ha hecho.

### ¿Puedo conseguir recompensas cambiando el reloj del dispositivo?
No. Cuando se detecta un retroceso del reloj, ese tramo no se liquida y la app te lo comunica.

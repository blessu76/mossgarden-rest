---
title: "Cómo subimos la primera compilación a TestFlight"
description: "Al terminar el MVP subimos la primera compilación interna, pero el script de despliegue nos frenó una vez por el camino."
copy_review: iris 2026-11-14
---
El primer MVP de Moss Garden, un juego idle para iOS, se subió a TestFlight como 1.0.0 (1) para pruebas internas después de que un script de despliegue frenara el primer intento. El procesamiento tardó unos tres minutos, y la compilación no se envió a revisión ni se abrió a testers externos.

## Qué incluía el MVP

El primer MVP reunía ocho plantas, liquidación sin conexión, estaciones, un libro de colección, guardado y ajustes. Lo subimos a TestFlight como 1.0.0 (1) para pruebas internas. El procesamiento tardó unos tres minutos, y no lo enviamos a revisión ni lo abrimos a testers externos.

## El primer intento falló

Cuando el script de despliegue ejecutó la puerta verde, una variable de entorno que significa «no subir el número de compilación» se coló en las pruebas y las rompió, y el script se detuvo ahí mismo. Gracias a esa parada, no se subió ninguna compilación defectuosa. Lo corregimos para que los procesos hijos ya no hereden el entorno exterior y volvimos a subirla.

Desplegar puede ser un fastidio, pero mantenemos la regla: si las pruebas no están en verde, no se publica nada.

## Preguntas frecuentes

### ¿Qué incluía la primera compilación de Moss Garden en TestFlight?
Ocho plantas, liquidación sin conexión, estaciones, un libro de colección, guardado y ajustes, subida como 1.0.0 (1) para pruebas internas.

### ¿Se ha enviado Moss Garden a revisión de la App Store?
No. Esta compilación solo se subió para pruebas internas y no la enviamos a revisión.

---
title: Los niveles los crea un solucionador, no la suerte
summary: Si mezclas las canicas al azar, algunos tableros no tienen solución. Por eso generamos todos los niveles de antemano y comprobamos que se pueden terminar.
lang: es
copy_review: iris 2026-11-15
date: 2026-11-15
time: 19:10
---
Los puzles de clasificar tienen una trampa: si mezclas las canicas al azar, algunas combinaciones simplemente no se pueden resolver. A nadie le gusta descubrirlo en el movimiento cuarenta.

## La decisión

Los niveles no se generan mientras juegas. Un solucionador los construye antes de publicar la app, y la app incluye el resultado como un archivo estático: para cada nivel, la disposición de las botellas y el **mínimo de movimientos** necesarios para resolverlo. La app solo lee los niveles a través de una pequeña interfaz, así que la forma de crearlos puede cambiar sin tocar las pantallas.

Lo elegimos porque un nivel ya construido tiene garantizada una solución, y porque conocer el mínimo permite que la app lo muestre junto a tu mejor resultado.

## Cómo se crea un nivel

- Se parte de n colores con una semilla aleatoria fija: n botellas llenas, más 2 vacías.
- Se busca una solución. El primer prototipo usó una búsqueda en profundidad con un tope de 60.000 estados.
- La búsqueda descarta los movimientos que no pueden ayudar: tocar una botella que ya está terminada, verter en botellas vacías más de una vez, pasar una única canica de una botella con una sola canica a una botella vacía.
- Un estado se guarda como la lista ordenada de botellas, de modo que dos disposiciones que solo difieren en el orden de las botellas cuentan como la misma.
- Después se calcula el mínimo de movimientos: búsqueda en anchura para los niveles pequeños y profundización iterativa para los grandes.
- Los niveles sin solución, ya resueltos o demasiado fáciles se descartan. Lo que queda se ordena de fácil a difícil.

## Comprobación

El plan incluye una prueba que vuelve a resolver cada nivel incluido, y la primera versión jugable apuntaba a tener al menos 30 niveles. La página de inicio ahora dice 150.

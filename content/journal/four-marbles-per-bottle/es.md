---
title: Cuatro canicas por botella: el reglamento completo
date: 2026-11-13
time: 22:28
summary: Las reglas de Bottled Marbles caben en unas pocas líneas. Aquí están, junto con las pequeñas decisiones que las rodean.
lang: es
copy_review: iris
---
Bottled Marbles es un rompecabezas de clasificación: mueve canicas entre botellas de vidrio hasta que cada botella contenga un solo color. El reglamento es corto a propósito.

## Las reglas, tal como están escritas

- Una botella contiene **4 canicas**. Un nivel con n colores tiene 4 × n canicas.
- Hay n + 2 botellas: n empiezan llenas y **2 empiezan vacías**.
- Puedes verter desde una botella que no esté vacía a una botella que no esté llena, y solo sobre una botella vacía o sobre una canica del mismo color.
- Viertes toda la tanda de canicas del mismo color que está arriba, hasta donde quepa en la botella de destino, y eso cuenta como **un movimiento**.
- Ganas cuando cada botella está vacía o llena de un solo color.

El número de colores crece con el nivel: `min(3 + floor((level + 1) / 2), 8)`, así que los primeros niveles tienen tres colores y los posteriores dejan de crecer en ocho.

## Cuatro y dos

La capacidad de cuatro y las dos botellas de reserva vienen directamente del primer prototipo. Las dos botellas vacías son el margen que hace posible verter, y no hemos necesitado cambiar ninguno de los dos números.

## Pequeñas decisiones que importan

- Tocar de nuevo la misma botella la deselecciona, y una botella vacía no se puede seleccionar.
- Tocar una botella en la que no puedes verter te lo indica y traslada tu selección a ella, en lugar de ignorar el toque en silencio.
- Deshacer es ilimitado y resta un movimiento del contador. Reiniciar devuelve el nivel a su disposición inicial.

Estas reglas salieron del primer prototipo jugable y se mantuvieron sin cambios en la app. El récord que guardamos de cada nivel es el menor número de movimientos que necesitaste.

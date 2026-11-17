---
title: Canicas que se distinguen sin necesidad del color
summary: Diez colores de canicas, diez símbolos, algunas pruebas de diseño en pantallas pequeñas y un botón que no se podía tocar.
lang: es
copy_review: iris
date: 2026-11-17
time: 17:00
---
Un juego en el que se ordena por colores tiene un problema evidente: hay jugadores que no distinguen los colores. La versión 6 de la app, que incluye el diseño Teal Glass, aborda ese problema y algunos otros más pequeños.

## Símbolos en las canicas

Hay diez colores de canicas y cada uno tiene además su propio **símbolo**. El color es la señal principal y el símbolo es el respaldo, de modo que un nivel sigue teniendo solución cuando dos tonos se parecen.

## Pruebas en pantallas pequeñas

Las pruebas de widgets dibujan las pantallas con 320 y 375 px de ancho, en modo oscuro y claro, con el texto ampliado al 200 %, y fallan ante cualquier desbordamiento. Esa matriz es barata de ejecutar y detecta el tipo de error que, de otro modo, solo aparece en el móvil pequeño de alguien.

Lo que aún no hemos hecho: esas pruebas son pruebas de widgets más capturas de un simulador de unos 393 px de ancho. Falta comprobarlo en un teléfono real con 320 o 375 px, y así lo dejamos escrito en nuestras notas.

## El botón bajo la vista con desplazamiento

Mientras construíamos la pantalla de inicio descubrimos que el botón de ajustes no respondía a los toques. La causa estaba en las capas: en la pila quedaba debajo de la vista con desplazamiento, que recogía todos los toques. Cambiar el orden de la pila lo arregló. Se corrigió en la misma versión que el rediseño.

## Lo que falta

Hay seis tapones y cinco estilos de botella ya diseñados, pero por ahora solo se incluye el aspecto predeterminado. La estructura puede crecer para acogerlos. Tampoco están aún las nuevas animaciones de vertido ni la respuesta háptica; el comportamiento actual se mantiene.

# Retroalimentación — Laboratorio 3: Estructuras de datos

**Estudiante:** Brayan Alexis Arango Orrego · **Laboratorio:** Laboratorio evaluativo 03 — Estructuras de datos
**Fecha límite:** 2026-11-01 23:59 · **Versión revisada:** commit `31a9b87`

Muy buen trabajo: el código es correcto y el informe se apoya en sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 17 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 24 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **96 / 100** |
| **Nota (0–5)** | **4.80** |

## 1. Corrección conceptual (17 / 20)
**Lo que hizo bien:**
- Explica bien la colisión con el ejemplo de las guías 10, 24 y 17 con `m = 7`, y compara encadenamiento con direccionamiento abierto.
- Justifica que la tabla hash no sirve para rangos porque no guarda las guías en orden, y propone el árbol de búsqueda para esa consulta.
- Recomienda una combinación razonable (tabla hash para consulta puntual y árbol equilibrado para rangos) y declara que el valor a 5.000.000 es una estimación.

**Lo que puede mejorar (y cómo corregirlo):**
- En la pregunta 4 dice que el árbol degenerado tiene altura cercana a 400.000, pero no estima cuántas comparaciones se hacen en total al insertar las 400.000 guías, solo las de una búsqueda.
  → *Cómo corregirlo:* piense cuántos nodos hay que recorrer para insertar la guía número 1, la 2, la 3... y sume ese recorrido sobre todas las guías; haga lo mismo para el árbol equilibrado y compare.
- Tampoco explica cómo el árbol responde "entre X y Y" ni cuánto cuesta.
  → *Cómo corregirlo:* describa en una o dos frases cómo se ubica X y cómo se sigue en orden hasta Y, y de qué depende el costo.
- En la pregunta 5 el cálculo para la lista es una multiplicación directa (×125). Dice que la curva es casi una línea recta, pero no lo justifica con sus propios números.
  → *Cómo corregirlo:* señale en sus datos qué pasa con el tiempo cada vez que n se duplica y use eso para explicar por qué es válido escalar así. Diga también qué número de casillas `m` usaría para la tabla con 5.000.000 de envíos.
- En direccionamiento abierto describe el funcionamiento, pero dice poco sobre su ventaja concreta frente al encadenamiento.
  → *Cómo corregirlo:* agregue qué se ahorra (por ejemplo, memoria de punteros) y qué se pierde cuando la tabla se llena.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Explica por qué la búsqueda de una guía inexistente en la lista recorre todos los nodos, `Θ(n)`.
- Explica que la tabla cuesta `Θ(1 + α)` porque solo se revisa la lista de una casilla, y nombra el supuesto de que las guías se reparten de forma pareja.
- Dice qué pasa si todas las guías caen en la misma casilla: la tabla se vuelve tan lenta como la lista.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- `ListaEnlazada` y `TablaHash` funcionan: las búsquedas exitosas e infructuosas dan el resultado correcto, la colisión con `m = 7` queda en la casilla 3 con longitud 3 y `factor_carga()` da 3/7.
- La tabla reutiliza la lista enlazada, `buscar` usa un ciclo `while` y no se usan `dict`, `set` ni `hash()`.
- Las pruebas cubren 25 colecciones aleatorias y varios casos límite.
- Todas las funciones tienen *type hints* y *docstrings* con `Args` y `Returns`.

## 4. Calidad del análisis de las gráficas (24 / 25)
**Lo que hizo bien:**
- Las dos gráficas están en el informe, con título, ejes rotulados con unidades y leyenda. La primera usa nueve valores de `n` y la segunda siete valores de `α`.
- En la pregunta 2 calcula el crecimiento de la lista (de 10.000 a 20.000 y de 20.000 a 40.000 guías, cerca de ×2) y lo relaciona con `Θ(n)`.
- Relaciona el aumento del tiempo de la tabla al subir `α` con `Θ(1 + α)`, y las cifras que cita coinciden con lo que muestran las gráficas.

**Lo que puede mejorar (y cómo corregirlo):**
- Para la tabla no calcula cuánto se multiplicó el tiempo entre dos valores consecutivos de `n`; solo dice que "se mantuvo cerca de 0,14 µs".
  → *Cómo corregirlo:* divida el tiempo de la tabla en un `n` entre el del `n` anterior, igual que hizo con la lista, y compare con lo esperado de `Θ(1)`.
- En el experimento B no calcula cuánto cambia el tiempo cuando `α` se multiplica (por ejemplo de 1 a 4 o de 4 a 10).
  → *Cómo corregirlo:* tome dos valores de `α` de su tabla, calcule el cociente de los tiempos y compárelo con el cociente de los `α`; explique por qué no son iguales (piense en el trabajo fijo que no depende de `α`).

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- La carpeta `laboratorios/lab3-estructuras-datos/` está en una ubicación válida y trae todos los archivos pedidos.
- El informe sigue el orden pedido, tiene las instrucciones para reproducir, y enlaza `estructuras.py`, `pruebas.py` y `medicion.py` donde corresponde. Las imágenes se ven con rutas relativas correctas.
- Hay cuatro commits del laboratorio, todos con mensajes descriptivos.

## ¿El código funciona?
Sí. Las pruebas terminan con "Todas las pruebas pasaron" y la medición corre en pocos segundos y genera las tres gráficas sin errores.

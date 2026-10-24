# Retroalimentación — Laboratorio 2: Dividir y vencer

**Estudiante:** Brayan Alexis Arango Orrego · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-10-21 23:59 · **Versión revisada:** commit `cb45003`

Excelente trabajo: un laboratorio completo, ordenado y bien sustentado con sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 19 / 20 |
| Calidad de la explicación teórica | 19 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 23 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **96 / 100** |
| **Nota (0–5)** | **4.80** |

## 1. Corrección conceptual (19 / 20)
**Lo que hizo bien:**
- Identificó que divide y vencerás empieza a ganar entre 10 y 50 elementos, con datos suyos, y explicó por qué con pocos datos la fuerza bruta es más rápida.
- Comparó con el máximo de un arreglo: mostró que dividir no mejora (`Θ(n)` en ambos casos) porque combinar cuesta poco y la recursión añade trabajo.
- Recomendó divide y vencerás y estimó el tiempo con 1.000.000 de registros (unas 4,4 horas contra 1,4 segundos), declarándolo como estimación y sin usar una regla de tres lineal.

**Lo que puede mejorar:**
- Podría precisar mejor en qué tamaño exacto se cruzan las curvas (por ejemplo, probando 20 o 30) y mencionar que la estimación depende de que el equipo y la memoria se comporten igual con series tan grandes.

## 2. Calidad de la explicación teórica (19 / 20)
**Lo que hizo bien:**
- Planteó `T(n) = 2T(n/2) + Θ(n)` explicando de dónde sale cada término.
- Resolvió con el método maestro (caso 2) y mostró que `n^(log₂ 2) = n` coincide con `f(n)`.
- Justificó el `Θ(n²)` de la fuerza bruta contando los `n(n+1)/2` tramos.

**Lo que puede mejorar:**
- Al resolver, diga expresamente que `f(n) = Θ(n^(log_b a))`, que es la condición que define el caso 2.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Las tres funciones dan resultados correctos en todos los casos pedidos y coinciden entre sí en listas aleatorias.
- `subarreglo_maximo` resuelve los tres casos, no llama a la fuerza bruta y no modifica la lista recibida.
- El código sigue PEP 8, con *type hints* y *docstrings* en cada función.
- Las pruebas comparan la suma (no los índices) y revisan que la lista no cambie.

## 4. Calidad del análisis de las gráficas (23 / 25)
**Lo que hizo bien:**
- La gráfica tiene título, ejes rotulados, leyenda y ambas curvas en los mismos ejes, con ocho tamaños; agregó además una versión log-log y una tabla.
- Calculó el factor al duplicar `n` para ambos algoritmos (≈ 4,08 y ≈ 2,11) y lo comparó con lo esperado. Las cifras coinciden con lo que muestra la gráfica publicada.

**Lo que puede mejorar:**
- Hizo la comparación con un solo par de tamaños. Repetirla con otro par (por ejemplo 1.000 → 2.000) daría más seguridad de que el patrón se sostiene.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- La carpeta está en `laboratorios/lab2-divide-y-vencer/`, con todos los archivos pedidos, enlaces al código en cada parte, imágenes que se ven y instrucciones de reproducción.
- Tiene cuatro commits con mensajes descriptivos.

## ¿El código funciona?
Sí. Las pruebas pasan, las dos soluciones coinciden con una comprobación independiente en listas aleatorias y la medición corre completa y genera las gráficas.

## Para el próximo laboratorio
- Repita la comparación de crecimiento con más de un par de tamaños.
- Indique con más precisión el tamaño donde cambia el ganador, agregando tamaños intermedios.
- Cuando resuelva recurrencias, escriba de forma explícita la condición del caso del método maestro.
- Mantenga los commits pequeños y descriptivos como en este laboratorio.

# Retroalimentación — Laboratorio 01: Fundamentos, complejidad y recurrencias

**Estudiante:** Brayan Alexis Arango Orrego · **Laboratorio:** Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias
**Fecha límite:** 2026-10-06 23:59 · **Versión revisada:** commit `640dc57`

Excelente trabajo: un informe completo, con datos propios y bien respaldado por sus mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 23 / 25 |
| Calidad de la explicación teórica | 24 / 25 |
| Corrección de la implementación | 16 / 20 |
| Calidad del análisis de las gráficas | 19 / 20 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **92 / 100** |
| **Nota (0–5)** | **4.60** |

## 1. Corrección conceptual (23 / 25)
**Lo que hizo bien:**
- Distingue bien entre que el resultado sea correcto y que llegue a tiempo, y nombra la restricción incumplida: las cuatro horas de la ventana.
- Explica por qué duplicar el servidor no basta, con sus propios datos (el lote creció 60 veces y el trabajo unas 3.600).
- Identifica dos perjuicios concretos para el paciente, dice quién asume el costo y propone verificar cada noche que la lista salga completa y ordenada.
- Conecta el tiempo de proceso con las horas de CPU acumuladas durante años.

**Lo que puede mejorar:**
- El ejemplo propio (descarga de la historia clínica) es real, pero es impreciso: no sabe la cantidad exacta de documentos ni la causa del fallo. Un ejemplo con cifras más firmas sería más sólido.
- La parte ambiental habla de horas de CPU, pero no llega a energía (por ejemplo, kWh) ni a su impacto.

## 2. Calidad de la explicación teórica (24 / 25)
**Lo que hizo bien:**
- Define peor caso, mejor caso y caso promedio indicando sobre qué conjunto de entradas se toma cada uno, con tamaño fijo.
- Justifica que usaría el peor caso por la ventana estricta, y deja la predicción escrita antes del experimento.
- Plantea la recurrencia de merge sort explicando cada término, la resuelve con el árbol de recursión paso a paso y la contrasta con el método maestro.
- Cuenta línea a línea las ejecuciones de insertion sort y presenta la tabla de complejidades.

**Lo que puede mejorar:**
- En la tabla de líneas, el costo total queda expresado con constantes sin sumarlo explícitamente hasta una fórmula final; un paso más de suma lo dejaría completo.

## 3. Corrección de la implementación (16 / 20)
**Lo que hizo bien:**
- `insertion_sort` y `merge_sort` ordenan bien los tres escenarios, no cambian la lista recibida y cuentan solo comparaciones entre elementos.
- `merge_sort` tiene su propia mezcla recursiva; los generadores usan semilla y dan listas de valores distintos.
- Casi todas las funciones tienen *docstring* y *type hints*.

**Lo que puede mejorar:**
- `generar_casi_ordenado` usa `sort` de Python para armar la parte ordenada. Es mejor construirla sin esa función para respetar la restricción de no usar ordenamientos de la librería.
- Algunas funciones de los scripts (`generar_lote`, `medir`, `correr_experimento`) no tienen todos los *type hints*, y sus *docstrings* no siguen el formato Google (sin Args ni Returns).
- `RANGO_MAXIMO` en `datos.py` no se usa.

## 4. Calidad del análisis de las gráficas (19 / 20)
**Lo que hizo bien:**
- Las tres gráficas tienen título, ejes con unidades y leyenda, y muestran las curvas pedidas en los mismos ejes.
- Identifica con evidencia el peor caso (C), el mejor (B) y el promedio (A), incluso comparando con la fórmula n(n−1)/4.
- Concluye que merge sort es mejor describiendo lo que hace cada curva y lo contrasta con las complejidades de 4.1.
- El concepto técnico recomienda un algoritmo, responde a la propuesta del servidor con un dato medido, extrapola a 1.200.000 registros declarándolo estimación y discute memoria y mantenimiento.

**Lo que puede mejorar:**
- Las curvas de merge sort y del escenario B quedan pegadas al eje; una escala logarítmica ayudaría a verlas mejor.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- La carpeta está en `laboratorios/lab1-fundamentos-complejidad-recurrencias/`, ubicación válida, con todos los archivos del entregable.
- El informe sigue el orden pedido, incrusta las gráficas con ruta que funciona, enlaza el código en cada parte e incluye instrucciones para reproducir.
- Tiene commits descriptivos que muestran el avance del laboratorio.

## ¿El código funciona?
Sí. Los dos algoritmos ordenan bien en mis pruebas y los dos scripts corren sin errores y generan las gráficas. Los comparaciones coinciden con las de su informe; los tiempos varían un poco según el equipo, como usted lo advierte.

## Para el próximo laboratorio
- Arme los datos de prueba sin usar funciones de ordenamiento de Python.
- Ponga *type hints* y *docstrings* completos (Args y Returns) en todas las funciones, incluidas las auxiliares.
- Quite el código que no se usa.
- Cierre el análisis ambiental con una estimación de energía, no solo de horas de CPU.
- Considere escala logarítmica en las gráficas cuando una curva domina a las demás.

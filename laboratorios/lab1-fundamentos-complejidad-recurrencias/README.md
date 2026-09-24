# Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias

**Estudiante:** Brayan Alexis Arango Orrego — Análisis de Algoritmos, 2026-2

> Convención usada en todo el informe: la lista final va en orden **descendente de índice de riesgo** (primero el paciente más grave). Generadores, algoritmos y conclusiones respetan esa misma regla.

## Cómo reproducir el experimento

1. Crear y activar el entorno (una sola vez, en la raíz del repositorio):

```bash
python -m venv venv
source venv/Scripts/activate    # Git Bash en Windows
# source venv/bin/activate      # Linux o macOS
pip install -r requirements.txt
```

2. Ejecutar cada parte:

```bash
cd laboratorios/lab1-fundamentos-complejidad-recurrencias
python parte3_casos.py          # Parte 3: imprime la tabla y crea 2 gráficas
python parte4_complejidad.py    # Parte 4: imprime la tabla y crea 1 gráfica
```

Notas de medición: los generadores usan semilla 42, así que las comparaciones se repiten con la misma versión de Python. La medición con `time.perf_counter()` envuelve solo la llamada al algoritmo, y cada tiempo reportado es la mediana de 3 repeticiones para suavizar el ruido del sistema operativo. Los milisegundos cambian de un equipo a otro; la forma de las curvas no.

## Parte 1 — Analizar el algoritmo antes de comprar hardware

Tamiza tiene hoy dos propiedades que conviene no confundir.

**Es correcto.** Un algoritmo de ordenamiento es correcto cuando recibe una lista y devuelve los mismos registros, pero organizados según el criterio solicitado. En este caso, insertion sort cumple con eso: durante los ocho años de uso de Tamiza no se ha encontrado una lista con registros perdidos o fuera de orden.

**No es viable.** En este caso no basta con que el resultado sea correcto, también tiene que estar listo a tiempo. El proceso empieza a las 2 de la mañana y la línea de llamadas abre a las 6, por lo que solo hay cuatro horas disponibles. Esa es la restricción que se está incumpliendo y ya ha provocado tres jornadas con la lista incompleta. La corrección y el tiempo de ejecución son aspectos diferentes: una revisa el resultado y la otra cuánto tarda en obtenerse.

**Por qué duplicar la velocidad no alcanza.** El problema no se debe solamente a que el equipo sea lento. El lote pasó de unos 20.000 registros a 1.200.000, es decir, creció 60 veces. Como insertion sort tiene un crecimiento proporcional a n², eso representa unas 3.600 veces más trabajo. Un procesador que sea el doble de rápido solo reduciría ese tiempo a la mitad. Mis mediciones muestran el mismo comportamiento: al duplicar n, el tiempo aumenta casi cuatro veces. Por ejemplo, en el escenario A pasó de 184,97 ms a 723,74 ms entre 3.200 y 6.400 registros. Por eso, cambiar solamente el hardware no soluciona el problema de fondo.

**Un caso propio.** Como afiliado a SURA, intenté descargar desde el portal mi historia clínica completa. Son cerca de 9 años de consultas, laboratorios y fórmulas, que calculo que pueden ser entre 150 y 250 documentos, aunque no conozco la cantidad exacta. La página se quedó cargando y no terminó de responder, así que tuve que recargarla y no pude obtener el archivo. Mi suposición es que la consulta funciona bien para historias más pequeñas, pero en mi caso pudo superar el tiempo máximo de espera de la sesión web. En este ejemplo, el problema fue el tiempo de respuesta y no la exactitud de los datos.

## Parte 2 — Responsabilidad ambiental y ética de la implementación

**Dimensión ambiental.** El tiempo de procesamiento también implica consumo de energía. Según la extrapolación de la Parte 4, insertion sort necesitaría unas 5,7 horas de CPU cada madrugada para ordenar un lote aleatorio de 1.200.000 registros, mientras que merge sort tardaría unos 3 segundos. Como el proceso se ejecuta todas las noches, la diferencia acumulada es considerable: unas 2.080 horas de procesador al año con insertion sort frente a unos 20 minutos con merge sort, y la plataforma lleva ocho años funcionando así. Además, cuando el proceso no alcanza a terminar, parte de esa energía se consume sin obtener una lista que pueda utilizarse correctamente.

**Dimensión ética.** Veo dos perjuicios concretos:

1. *Un paciente de alto riesgo no recibe la llamada a tiempo.* Si la lista sale incompleta o sin ordenar, alguien con un índice cercano a 1000 puede quedar al final de la cola o fuera de la jornada. El costo lo asume **el paciente**: su valoración cardiovascular se retrasa sin que haya tenido forma de enterarse ni de reclamar.
2. *Los cupos de valoración se los llevan pacientes de menor riesgo.* Las citas disponibles cada día son limitadas. Si la lista va desordenada, pacientes de riesgo bajo ocupan esos cupos y el de riesgo alto, cuando por fin lo llaman, encuentra la agenda llena. De nuevo el costo recae primero sobre **el paciente** más grave; la Secretaría también pierde, porque paga consultas que no se asignaron según la prioridad clínica que el programa promete.

En ambos casos, el problema termina afectando al paciente, que no fue quien tomó la decisión sobre el sistema. La responsabilidad de corregirlo corresponde al equipo técnico encargado del proceso y a la Secretaría, que debe decidir si se realiza el cambio.

**El orden define la prioridad de llamada.** Por esta razón, un error en el ordenamiento también puede afectar la prioridad con la que se contacta a los pacientes. Esto impone una obligación adicional, más allá del tiempo: garantizar que el orden sea verificable. Para eso se debe comprobar cada noche que la salida tenga la misma cantidad de registros que la entrada y que los índices estén realmente en orden descendente. Este chequeo es lineal y tiene un costo bajo. También es importante que, si el proceso no termina, el sistema lo reporte claramente en lugar de entregar una lista incompleta como si fuera válida.

## Parte 3 — Peor caso, mejor caso y caso promedio, demostrados en Python

[Código de la Parte 3](parte3_casos.py) · funciones en [algoritmos.py](algoritmos.py) · generadores en [datos.py](datos.py)

### 3.1 — Explicación

Fijo un tamaño n y llamo **E(n)** al conjunto de todas las listas posibles de n índices de riesgo distintos, es decir, todas sus permutaciones. Si C(x) es el número de comparaciones que hace el algoritmo con la entrada x:

- **Peor caso:** máx { C(x) : x ∈ E(n) }, la entrada de ese tamaño que más comparaciones exige.
- **Mejor caso:** mín { C(x) : x ∈ E(n) }, la que menos exige.
- **Caso promedio:** el valor esperado de C(x) cuando x se escoge en E(n) con todas las permutaciones igual de probables.

Los tres se comparan siempre con n fijo: no tiene sentido llamar "peor" a una entrada comparándola con otra de distinto tamaño.

**Para aprobar el paso a producción tendría en cuenta principalmente el peor caso**, porque las cuatro horas son un límite que se debe cumplir todas las noches. Además, Tamiza no controla cómo llega la información. Por ejemplo, una nueva migración desde el sistema legado podría generar nuevamente datos en orden inverso. Que el tiempo promedio esté dentro de las cuatro horas no garantiza que una noche determinada también lo esté.

**Predicción:**

| Escenario | Lo que espero para insertion sort | Razón |
|---|---|---|
| C — orden inverso | Peor caso | Cada registro nuevo es mayor que todos los anteriores y debe desplazarse hasta el comienzo de la parte ya ordenada. |
| B — casi ordenado | El mejor de los tres | El 98 % inicial ya está en su sitio y cuesta una comparación por registro; solo el 2 % final hace trabajo real. |
| A — aleatorio | Intermedio, cercano al caso promedio | Es una permutación al azar, que es justo lo que modela el promedio. |

### 3.2 — Demostración experimental

Valores que imprime `parte3_casos.py` (tiempo = mediana de 3 repeticiones):

| n | A — comparaciones | A — tiempo (ms) | B — comparaciones | B — tiempo (ms) | C — comparaciones | C — tiempo (ms) |
|---|---|---|---|---|---|---|
| 100 | 2.648 | 0,16 | 100 | 0,01 | 4.950 | 0,26 |
| 200 | 10.534 | 0,54 | 202 | 0,01 | 19.900 | 0,99 |
| 400 | 38.744 | 2,17 | 416 | 0,02 | 79.800 | 5,36 |
| 800 | 159.945 | 12,64 | 864 | 0,06 | 319.600 | 17,32 |
| 1.600 | 641.308 | 48,33 | 1.851 | 0,13 | 1.279.200 | 71,64 |
| 3.200 | 2.594.787 | 184,97 | 4.180 | 0,28 | 5.118.400 | 270,60 |
| 6.400 | 10.243.431 | 723,74 | 10.700 | 0,74 | 20.476.800 | 1.166,72 |

![Gráfica: comparaciones de insertion sort según n, escenarios A, B y C](graficas/parte3_comparaciones.png)

![Gráfica: milisegundos de insertion sort según n, escenarios A, B y C](graficas/parte3_tiempo.png)

- **Peor caso: C.** Es la curva más alta en ambas gráficas. Su conteo en n = 6.400 es 20.476.800, igual a n(n−1)/2 para ese n: el generador inverso produce justo la entrada que obliga a mover cada registro hasta el principio.
- **Mejor caso: B.** 10.700 comparaciones en n = 6.400, casi sobre el eje. El desglose cuadra con el código: el bloque ordenado aporta una comparación por elemento (6.271) y reacomodar los 128 registros finales entre ellos cuesta 4.426 (lo medí ordenando esa cola por separado). No baja al mínimo teórico de n − 1 = 6.399 porque la cola llega desordenada.
- **Caso promedio: A.** 10.243.431 comparaciones contra las n(n−1)/4 = 10.238.400 esperadas para una permutación aleatoria, un 0,05 % de diferencia. En la gráfica, A queda más o menos a media altura de C.

**Contraste con la predicción.** Los resultados coincidieron con lo esperado en los tres escenarios. Lo que no esperaba era que la diferencia entre B y C fuera tan grande: en n = 6.400, B queda casi 1.900 veces por debajo de C. También se puede ver que B no crece de manera totalmente lineal. Al pasar de 3.200 a 6.400 elementos, sus comparaciones aumentaron 2,56 veces, debido al trabajo adicional que genera la cola del 2 %.

## Parte 4 — Complejidad de merge sort e insertion sort: cálculo y validación

[Código de la Parte 4](parte4_complejidad.py) · `merge_sort` e `insertion_sort` en [algoritmos.py](algoritmos.py)

### 4.1 — Cálculo teórico

**Recurrencia de merge sort**

```
T(n) = 2·T(n/2) + Θ(n),   n > 1
T(1) = Θ(1)
```

| Término | Qué representa en `merge_sort` |
|---|---|
| 2 | Dos llamadas recursivas: `merge_sort(lista[:medio])` y `merge_sort(lista[medio:])`. |
| n/2 | Cada llamada recibe la mitad de los elementos (`medio = len(lista) // 2`). |
| Θ(n) | Trabajo fuera de la recursión: los dos cortes copian n elementos y `_mezclar` hace a lo sumo n − 1 comparaciones y n `append`. |
| T(1) | Una lista de 0 o 1 elementos se devuelve sin comparar. |

**Método elegido: árbol de recursión**, con c·n como costo no recursivo.

```
                     c·n                       nivel 0:  1 nodo   × c·n    = c·n
                  /       \
             c·n/2         c·n/2               nivel 1:  2 nodos  × c·n/2  = c·n
             /   \         /   \
        c·n/4  c·n/4   c·n/4  c·n/4            nivel 2:  4 nodos  × c·n/4  = c·n
          ...                                     ...
    c   c   c   c   ...   c   c   c   c        nivel h:  n hojas  × c      = c·n
```

- En el nivel i hay 2^i nodos de tamaño n/2^i, así que ese nivel cuesta 2^i · c·n/2^i = c·n. Todos los niveles cuestan lo mismo.
- Altura: los subproblemas llegan a tamaño 1 cuando n/2^h = 1, o sea h = log₂ n. Hay log₂ n + 1 niveles.
- Total: T(n) = c·n·(log₂ n + 1) = c·n·log₂ n + c·n = **Θ(n log n)**.

Contraste con el método maestro: a = 2, b = 2, f(n) = Θ(n) y n^(log₂ 2) = n; f(n) es del mismo orden que n^(log_b a), así que aplica el caso 2 y da Θ(n log n), igual que el árbol.

**Cota de insertion sort, contando ejecuciones por línea** (código real de `algoritmos.py`):

```
 1  lista = datos.copy()
 2  comparaciones = 0
 3  for i in range(1, len(lista)):
 4      clave = lista[i]
 5      j = i - 1
 6      while j >= 0:
 7          comparaciones += 1
 8          if lista[j] < clave:
 9              lista[j + 1] = lista[j]
10              j -= 1
11          else:
12              break
13      lista[j + 1] = clave
14  return lista, comparaciones
```

Sea t_i el número de comparaciones de elementos en la iteración i (1 ≤ t_i ≤ i) y s_i el número de desplazamientos (s_i ≤ t_i).

| Líneas | Veces que se ejecutan |
|---|---|
| 1 | 1 (copia n elementos) |
| 2, 14 | 1 |
| 3 | n |
| 4, 5, 13 | n − 1 |
| 6 | a lo sumo Σ (t_i + 1) |
| 7, 8 | Σ t_i |
| 9, 10 | Σ s_i ≤ Σ t_i |
| 11, 12 | a lo sumo n − 1 |

Las sumas recorren i = 1, …, n − 1. Juntando constantes queda T(n) = k·Σ t_i + a·n + b: lo único que varía según cómo llegue la entrada es Σ t_i.

- **Mejor caso** (entrada ya descendente): el primer `if` falla de inmediato, t_i = 1 y Σ t_i = n − 1, así que T(n) = **Θ(n)**. Lo comprobé pasando `list(range(100, 0, -1))`: devolvió 99 comparaciones.
- **Peor caso** (entrada ascendente): cada clave se desplaza hasta la posición 0, t_i = i y Σ t_i = n(n−1)/2, así que T(n) = **Θ(n²)**. Coincide exactamente con el escenario C.
- **Caso promedio** (permutaciones equiprobables): en esperanza t_i ≈ i/2 y Σ t_i ≈ n(n−1)/4, así que T(n) = **Θ(n²)**. Coincide con el escenario A (0,05 %).

**Tabla de complejidades**

| Algoritmo | Mejor caso | Caso promedio | Peor caso |
|---|---|---|---|
| Insertion sort | Θ(n) | Θ(n²) | Θ(n²) |
| Merge sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |

Merge sort no cambia de columna porque su punto de corte depende solo de la longitud (`len(lista) // 2`), nunca del contenido: el árbol es idéntico para cualquier entrada del mismo tamaño.

### 4.2 — Validación experimental

Valores que imprime `parte4_complejidad.py` (escenario A, mediana de 3 repeticiones):

| n | Insertion sort (ms) | Merge sort (ms) |
|---|---|---|
| 100 | 0,13 | 0,11 |
| 200 | 0,49 | 0,23 |
| 400 | 1,89 | 0,51 |
| 800 | 11,97 | 1,08 |
| 1.600 | 35,05 | 2,35 |
| 3.200 | 138,35 | 4,98 |
| 6.400 | 583,82 | 10,69 |

![Gráfica: milisegundos según n, insertion sort frente a merge sort, escenario A](graficas/parte4_tiempo.png)

- **Para Tamiza es más adecuado merge sort.** En la gráfica se observa que insertion sort aumenta mucho más rápido: pasa de 138,35 ms a 583,82 ms entre 3.200 y 6.400 registros (×4,22). Merge sort pasa de 4,98 ms a 10,69 ms en el mismo rango (×2,15). Para n = 6.400, la diferencia entre ambos llega a 54,6 veces.
- **Coincide con 4.1.** Duplicar n en un algoritmo Θ(n²) multiplica el tiempo por 4; en uno Θ(n log n) lo multiplica por 2·log(2n)/log(n), que para n = 3.200 da ≈ 2,17. Medí 4,22 y 2,15. El conteo de comparaciones, independiente del hardware, confirma lo mismo: con 6.400 registros insertion sort hace 10.243.431 y merge sort 72.940, unas 140 veces menos.
- **Tamaños pequeños.** En el rango de la guía merge sort ya gana desde n = 100 (0,11 contra 0,13 ms), así que la gráfica no muestra cruce. Para ubicarlo medí aparte n = 20 y n = 50, y ahí insertion sort fue más rápido (0,012 contra 0,029 ms y 0,060 contra 0,076 ms). Cada llamada recursiva de merge sort crea listas y marcos de función nuevos, un costo fijo que en listas muy cortas pesa más que su ventaja asintótica. El cruce queda entre 50 y 100 elementos, muy lejos del 1.200.000 de Tamiza.

### 4.3 — Concepto técnico a la Secretaría de Salud

**A:** Equipo de ingeniería — Secretaría de Salud departamental
**Ref.:** Ordenamiento nocturno de la plataforma Tamiza y propuesta de cambio de servidor

**Recomendación.** Cambiar el algoritmo del proceso nocturno a merge sort y evaluar la compra del servidor después de comprobar el comportamiento del nuevo algoritmo con los datos reales.

**Criterio.** El lote puede cambiar de un día a otro, por lo que no sería conveniente elegir el algoritmo basándose únicamente en los datos de un día específico. Además, el equipo no quiere mantener una implementación distinta para cada canal, así que necesita un solo algoritmo que funcione bien con cualquiera de los tres. Merge sort depende principalmente del tamaño de la lista y mantiene una complejidad de Θ(n log n) en los tres escenarios. Insertion sort depende mucho más del orden de entrada. En mis pruebas con n = 6.400 pasó de 0,74 ms con un lote casi ordenado a 1.166,72 ms con uno invertido. Una nueva migración desde el sistema legado podría cambiar completamente el comportamiento del proceso.

**¿Cabe en cuatro horas?** Los valores de la tabla son **estimaciones extrapoladas**, no mediciones. El lote más grande que ejecuté fue de 6.400 registros y 1.200.000 es 187,5 veces más grande. No usé regla de tres sino el crecimiento de cada algoritmo: con Θ(n²) el tiempo escala por 187,5² ≈ 35.156 y con Θ(n log n) por 187,5 × log(1.200.000)/log(6.400) ≈ 300. Supongo el mismo equipo y que las curvas conservan su forma.

| Algoritmo | Escenario | Medido (n = 6.400) | Estimado (n = 1.200.000) | ¿Cabe en 4 h? |
|---|---|---|---|---|
| Insertion sort | A — aleatorio | 583,82 ms | ≈ 5 h 42 min | No |
| Insertion sort | C — inverso | 1.166,72 ms | ≈ 11 h 24 min | No |
| Merge sort | A — aleatorio | 10,69 ms | ≈ 3 s | Sí, con amplio margen |

Estos resultados ayudan a explicar las tres fallas recientes del proceso.

**Sobre la compra del servidor.** Con n = 6.400 y el escenario A (gráfica `parte4_tiempo.png`), merge sort fue 54,6 veces más rápido que insertion sort. Comprar un equipo más rápido podría reducir los tiempos, pero no cambia la complejidad del algoritmo. Incluso suponiendo que el nuevo servidor sea el doble de rápido, insertion sort todavía tardaría unas 2 h 51 min con un lote aleatorio y unas 5 h 42 min con uno invertido. En este último caso seguiría superando las cuatro horas. Además, como el trabajo de insertion sort crece cuadráticamente, el problema volvería a aparecer al aumentar el tamaño de los datos. Por eso no recomiendo la compra como solución al problema.

**Consideraciones distintas del tiempo.**

- *Memoria:* merge sort necesita espacio auxiliar proporcional a n. Con `tracemalloc` medí en n = 6.400 un pico de unos 205 KB frente a unos 50 KB de insertion sort. Es un costo real, pero pequeño al lado de las horas de CPU.
- *Mantenimiento:* la función propuesta tiene la misma firma que la actual en `algoritmos.py` (recibe la lista y devuelve la lista ordenada), así que el cambio queda aislado y no obliga a tocar el resto de la plataforma.
- *Verificación:* conviene acompañar el cambio con un chequeo al final del proceso (cantidad de registros y orden descendente) y una alerta si no termina a tiempo, para que nadie en la línea de llamadas trabaje con una lista parcial sin saberlo.

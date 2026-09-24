# Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias

**Nombre:** Brayan Alexis Arango Orrego
**Curso:** Análisis de Algoritmos
**Caso:** Plataforma Tamiza — Secretaría de Salud departamental

Todo el ordenamiento de este laboratorio se hace de mayor a menor índice de riesgo, que es el orden en que Tamiza necesita la lista de llamadas del día. Los tres generadores de escenarios, los dos algoritmos y el análisis de los casos usan ese mismo criterio de forma consistente.

## Cómo reproducir el experimento

Desde la raíz del repositorio, con el entorno virtual activado:

```bash
python -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Ya con el entorno activo, parado en la carpeta de este laboratorio:

```bash
cd laboratorios/lab1-fundamentos-complejidad-recurrencias
python parte3_casos.py         # tabla de la Parte 3 y sus dos gráficas
python parte4_complejidad.py   # tabla de la Parte 4 y su gráfica
```

Cada script imprime en consola las mismas cifras que aparecen en las tablas de este informe y escribe sus imágenes en `graficas/`. Los generadores usan una semilla fija (42), así que el conteo de comparaciones se repite en cualquier máquina con la misma versión de Python; los tiempos sí cambian unos milisegundos entre corridas y entre equipos, porque dependen del hardware y de qué más esté corriendo en ese momento.

Cada punto de las tablas y gráficas de este informe es la mediana de tres corridas, tal como lo hace `parte3_casos.py` y `parte4_complejidad.py` (función `medir`). El cronómetro (`time.perf_counter()`) encierra únicamente la llamada al algoritmo: el lote se construye antes de arrancarlo.

## Parte 1 — Analizar el algoritmo antes de comprar hardware

Un algoritmo es correcto cuando, para cualquier entrada válida, entrega la salida que pide la especificación. En Tamiza eso significa que la lista de salida tiene los mismos 1.200.000 registros que entraron y queda ordenada de mayor a menor índice de riesgo, sin importar en qué orden hayan llegado. Insertion sort cumple eso desde hace ocho años: nunca se ha reportado una lista mal ordenada.

La eficiencia es otra cosa: es si el algoritmo entrega esa salida correcta dentro del recurso disponible, que en este caso es tiempo de CPU del servidor nocturno entre las 2:00 a. m. y las 6:00 a. m. Esa ventana de cuatro horas es la restricción concreta que el sistema está incumpliendo, y es la razón por la que tres veces en las últimas semanas el centro de contacto trabajó con una lista parcial. La corrección se verifica mirando la salida; el cumplimiento de la ventana se verifica cronometrando la ejecución. Por eso lo primero no implica lo segundo: el algoritmo puede seguir dando la respuesta exacta y entregarla a las diez de la mañana, cuando el centro de contacto ya lleva cuatro horas llamando con datos incompletos.

Duplicar la velocidad del servidor no resuelve el problema de fondo porque actúa sobre la constante del algoritmo, no sobre su crecimiento. Cuando la plataforma se escribió, el lote era de unos 20.000 registros; hoy son 1.200.000, sesenta veces más. Como insertion sort hace un número de comparaciones del orden de n², multiplicar los datos por 60 multiplica el trabajo por cerca de 3.600 veces. Un servidor del doble de velocidad divide el tiempo entre dos: un factor 2 contra un crecimiento acumulado de 3.600. Y ese alivio se agota solo: si el programa suma más municipios y el lote pasa a, por ejemplo, 1.700.000 registros (un 40 % más), el trabajo casi se duplica otra vez y la ventana vuelve a romperse, esta vez con el contrato del servidor ya firmado.

Algo parecido me pasó a mí como usuario de la plataforma de SURA, mi EPS. Intenté descargar mi historia clínica completa desde el portal, acumulada en unos 9 años como paciente — entre consultas, resultados de laboratorio y fórmulas, calculo que son del orden de 150 a 250 registros, aunque no tengo la cifra exacta. La página se quedó cargando y nunca volvió a responder: no hubo un mensaje de error, simplemente dejó de reaccionar y tocó recargarla. No sé qué hace el backend con esa consulta, pero el síntoma es el mismo que Tamiza: en algún punto el proceso que arma ese reporte incumplió el límite de tiempo de respuesta que el navegador o el propio servidor tolera antes de cortar la conexión. El dato no era gigante para estándares de una empresa, pero fue suficiente para que algo pensado para historiales cortos dejara de responder con uno más largo.

## Parte 2 — Responsabilidad ambiental y ética de la implementación

**Dimensión ambiental.** El tiempo de ejecución del proceso nocturno es tiempo de CPU trabajando al máximo, y esa CPU consume energía mientras lo hace. Con mis propias mediciones (ver Parte 4), extrapolar insertion sort a 1.200.000 registros da unas 5 horas y 42 minutos de procesador en el escenario aleatorio; merge sort, en cambio, se estima en apenas unos 3 segundos. Esa diferencia de horas de CPU activa se traduce directamente en consumo eléctrico. Vista una sola madrugada, la diferencia entre los dos algoritmos puede parecer un detalle; el problema es que el proceso corre *todas* las madrugadas, y la plataforma lleva ocho años en producción. Un algoritmo cuadrático no gasta energía una vez: la gasta cada noche, de forma acumulada, y ese gasto crece con el cuadrado del tamaño del lote cada vez que el programa se amplía a más municipios. Comprar el servidor del doble de velocidad no ayuda en esta dimensión: una máquina más rápida generalmente consume más vatios por hora, y el trabajo que hay que hacer sigue siendo el mismo.

**Dimensión ética.** La primera forma concreta de daño es la que recae sobre el paciente. Cuando el proceso no termina a tiempo y el centro de contacto trabaja con una lista parcial o desordenada, un paciente de alto riesgo puede quedar detrás de pacientes de menor riesgo en la cola de llamadas, o directamente no aparecer ese día. **El costo de ese error lo asume primero el paciente**: un retraso en su valoración médica que, en un programa de tamizaje cardiovascular, puede no ser recuperable. El paciente no tomó ninguna decisión técnica y no tiene forma de saber que el algoritmo que ordena su prioridad clínica no alcanzó a correr completo esa madrugada.

La segunda forma de daño recae sobre el operador del centro de contacto: recibe una lista sin garantía de que esté bien ordenada y no tiene manera de saberlo desde su puesto de trabajo. Llama de arriba hacia abajo confiando en que el orden refleja el riesgo real. Si más adelante se revisa por qué se contactó tarde a un paciente grave, lo que queda registrado es el nombre del operador junto a cada llamada, no la causa técnica de fondo. Aun así, sostengo que el costo mayor sigue siendo del paciente: el operador cumplió su trabajo con la información que le dieron, mientras que el paciente sufre la consecuencia clínica directa sin haber tenido ninguna forma de participar o de saber que algo estaba mal.

La responsabilidad de que esto pase es de quien decidió mantener el algoritmo sin revisarlo a pesar de conocer que la ventana ya se estaba incumpliendo: el equipo técnico que sostiene la plataforma y la Secretaría que aprueba (o pospone) los cambios.

Hay una tensión propia de este caso que va más allá del tiempo: el orden de la lista decide a quién se llama primero. Eso convierte al criterio de ordenamiento en una decisión con consecuencias clínicas, no solo en un detalle de implementación. Cuando dos pacientes tienen el mismo índice de riesgo, algo tiene que desempatar entre ellos, y ese "algo" queda definido por cómo está escrito el algoritmo, casi siempre sin que nadie lo haya discutido explícitamente. Esto impone una obligación adicional sobre la corrección del ordenamiento: que sea **estable y trazable** — que ante índices iguales el resultado sea siempre el mismo, siguiendo un criterio declarado (por ejemplo, cuál registro lleva más tiempo pendiente), y que quede registro de con qué índice y en qué posición entró cada paciente al proceso. Un algoritmo que ordena "bien" en el sentido técnico pero desempata de forma arbitraria cumple la especificación y aun así reparte la atención médica de forma injusta.

## Parte 3 — Peor caso, mejor caso y caso promedio, demostrados en Python

Código de esta parte: [parte3_casos.py](parte3_casos.py). Los algoritmos instrumentados están en [algoritmos.py](algoritmos.py) y los tres generadores de escenarios en [datos.py](datos.py).

### 3.1 — Explicación

Los tres casos no son tres entradas puntuales: son tres formas de resumir el costo del algoritmo sobre el conjunto de *todas* las entradas posibles de un mismo tamaño fijo n. Se fija n, se considera el conjunto de todas las listas de n índices de riesgo distintos que se le pueden dar al algoritmo, y sobre ese conjunto se toma:

- **Peor caso**: el máximo del número de comparaciones entre todas las entradas de tamaño n. Es la entrada específica que más le cuesta al algoritmo.
- **Mejor caso**: el mínimo del número de comparaciones sobre ese mismo conjunto de entradas de tamaño n.
- **Caso promedio**: el promedio del número de comparaciones sobre ese conjunto, asumiendo que todas las permutaciones de los n índices son igual de probables (es el supuesto usual, y el que uso aquí).

Decir "el caso malo" sin aclarar sobre qué conjunto de entradas de qué tamaño se toma el máximo no dice nada, porque el costo de un algoritmo no es un número fijo: es una función que depende tanto del tamaño como de la forma de la entrada.

**¿Cuál usaría para decidir si Tamiza entra en producción?** El peor caso. La ventana de cuatro horas no es una meta que se cumple en promedio: es un límite que se cumple o se incumple cada madrugada, y el equipo de Tamiza no controla cómo llega el lote — el canal de origen puede cambiar sin aviso (una migración, un reproceso distinto, un laboratorio que empieza a subir los datos de otra forma). Diseñar para el promedio significa que el proceso cabe "casi siempre", y ese "casi" es precisamente la madrugada en que el centro de contacto abre con una lista incompleta. Si el peor caso cabe en la ventana, cualquier entrada cabe.

**Predicción antes de medir.** Ordenando de mayor a menor, espero que el **escenario C sea el peor caso**: llega exactamente al revés de lo que Tamiza necesita, así que cada registro nuevo debe recorrer toda la porción ya ordenada antes de encontrar su lugar. Espero que el **escenario B sea el mejor de los tres** (aunque no el mejor caso teórico absoluto, que sería la lista completa ya ordenada): el 98 % ya viene en el orden final, y solo el 2 % restante tiene trabajo por hacer. Y espero que el **escenario A quede en la mitad**, como aproximación al caso promedio, por ser una permutación aleatoria de los índices — que es justamente la situación que ese promedio modela.

### 3.2 — Demostración experimental

Medición de `insertion_sort` sobre los tres escenarios, siete tamaños de entrada, mediana de tres corridas:

| n | A — comparaciones | A — tiempo (ms) | B — comparaciones | B — tiempo (ms) | C — comparaciones | C — tiempo (ms) |
|---|---|---|---|---|---|---|
| 100 | 2.648 | 0,16 | 100 | 0,01 | 4.950 | 0,26 |
| 200 | 10.534 | 0,54 | 202 | 0,01 | 19.900 | 0,99 |
| 400 | 38.744 | 2,17 | 416 | 0,02 | 79.800 | 5,36 |
| 800 | 159.945 | 12,64 | 864 | 0,06 | 319.600 | 17,32 |
| 1.600 | 641.308 | 48,33 | 1.851 | 0,13 | 1.279.200 | 71,64 |
| 3.200 | 2.594.787 | 184,97 | 4.180 | 0,28 | 5.118.400 | 270,60 |
| 6.400 | 10.243.431 | 723,74 | 10.700 | 0,74 | 20.476.800 | 1.166,72 |

![Comparaciones de insertion sort frente al tamaño de entrada en los tres escenarios](graficas/parte3_comparaciones.png)

![Tiempo de ejecución de insertion sort frente al tamaño de entrada en los tres escenarios](graficas/parte3_tiempo.png)

**Cuál escenario resultó el peor caso.** El **C**, orden inverso. Su curva queda por encima de las otras dos en ambas gráficas. En n = 6.400 hizo 20.476.800 comparaciones, y ese número coincide de forma exacta con la fórmula del peor caso teórico: n(n−1)/2 = 6.400 × 6.399 / 2 = 20.476.800. No es una aproximación — es el valor exacto, lo que confirma que el generador `generar_inverso` está produciendo, en efecto, el peor caso real del algoritmo.

**Cuál resultó el mejor.** El **B**, casi ordenado. En la gráfica de comparaciones queda pegado al eje horizontal: en n = 6.400 hizo 10.700 comparaciones contra 20.476.800 del escenario C, casi 1.914 veces menos, y 0,74 ms contra 1.166,72 ms. No es el mejor caso teórico absoluto (que serían 6.399 comparaciones para una lista ya completamente ordenada), porque el 2 % final del lote (128 registros en n = 6.400) todavía se reordena entre sí — el primer 98 % solo aporta una comparación por elemento (unas 6.271), y el resto del conteo (unas 4.400) sale de reordenar esos 128 registros entre ellos, algo cercano a lo que predice un insertion sort de ese tamaño más pequeño sobre sí mismo.

**Cuál se aproxima al caso promedio.** El **A**, aleatorio. En n = 6.400 midió 10.243.431 comparaciones, y el valor esperado bajo el supuesto de permutaciones equiprobables es n(n−1)/4 = 10.238.400 — una diferencia de apenas 0,05 %, coherente con el ruido de una sola muestra aleatoria. En la gráfica, la curva de A queda casi exactamente a la mitad entre C y el eje, que es justo lo que predice la teoría: la mitad del trabajo del peor caso.

**Contraste con la predicción de 3.1.** El experimento no contradijo la predicción: los tres escenarios quedaron en el orden esperado (C peor, B mejor, A en la mitad), y los tres conteos caen sobre las fórmulas teóricas correspondientes. Lo que si me sorprendió fue la magnitud de la diferencia entre B y los otros dos: esperaba que B fuera claramente el mejor, pero no que en la gráfica quedara prácticamente invisible frente a A y C. Vale aclarar que B sigue siendo cuadrático, no lineal: de n = 3.200 a n = 6.400 sus comparaciones se multiplicaron por 2,56, más que el factor 2 de un crecimiento lineal — solo que con una constante mucho más pequeña que la de A o C.

## Parte 4 — Complejidad de merge sort e insertion sort: cálculo y validación

Código de esta parte: [parte4_complejidad.py](parte4_complejidad.py), con `merge_sort` e `insertion_sort` definidos en [algoritmos.py](algoritmos.py).

### 4.1 — Cálculo teórico

**Planteamiento de la recurrencia de merge sort**, siguiendo la implementación de `merge_sort` en `algoritmos.py`:

```
T(n) = 2·T(n/2) + Θ(n)      para n > 1
T(1) = Θ(1)
```

- **2**: es el número de subproblemas. Cada llamada corta la lista en dos mitades y se llama recursivamente sobre cada una (`merge_sort(lista[:medio])` y `merge_sort(lista[medio:])`).
- **n/2**: es el tamaño de cada subproblema, porque el corte es exactamente por la mitad.
- **Θ(n)**: es el costo de lo que no es recursivo — las dos copias que produce el slicing y la mezcla en `_mezclar`, que recorre las dos mitades con dos índices que solo avanzan, haciendo como máximo n−1 comparaciones y construyendo una lista de n elementos.
- **T(1) = Θ(1)**: caso base — una lista de un solo elemento ya está ordenada, la función retorna de inmediato sin comparar nada.

**Resolución por árbol de recursión.** Llamo cn al costo del término no recursivo en cada nivel.

```
Nivel 0:                         T(n)                              costo: c·n

Nivel 1:                T(n/2)          T(n/2)                     costo: 2·c(n/2)      = c·n

Nivel 2:           T(n/4)  T(n/4)   T(n/4)  T(n/4)                 costo: 4·c(n/4)      = c·n

  ...                                                                     ...

Nivel k:            2^k subproblemas, cada uno de tamaño n/2^k      costo: 2^k·c(n/2^k)  = c·n

  ...                                                                     ...

Nivel log2(n):      n subproblemas de tamaño 1                     costo: n·c(1)        = Θ(n)
```

- **Costo por nivel**: en el nivel k hay 2^k subproblemas de tamaño n/2^k, así que el costo de ese nivel es 2^k · c·(n/2^k) = c·n — el mismo en todos los niveles, porque lo que se gana en tamaño de subproblema se pierde en cantidad de subproblemas.
- **Número de niveles**: el tamaño en el nivel k es n/2^k; se llega a las hojas cuando n/2^k = 1, es decir k = log₂n. Contando desde el nivel 0, hay log₂n + 1 niveles.
- **Costo total**: T(n) = c·n·(log₂n + 1) = c·n·log₂n + c·n. El término dominante es n·log n, así que T(n) = Θ(n log n).

**Verificación por el método maestro**, con a = 2, b = 2, f(n) = Θ(n): n^(log_b a) = n^(log₂2) = n¹ = n. Como f(n) = Θ(n) = Θ(n^(log_b a)), se cumple la condición del **caso 2** del método maestro, que concluye T(n) = Θ(n^(log_b a) · log n) = Θ(n log n). Coincide con el resultado del árbol.

**Cota de insertion sort, línea a línea.** Sobre el código de `insertion_sort` en `algoritmos.py`. Llamo n al tamaño de la lista; para cada iteración i (de 1 a n−1), c_i es el número de comparaciones entre elementos que hace esa iteración, con 1 ≤ c_i ≤ i.

| Línea | Instrucción | Costo | Veces que se ejecuta |
|---|---|---|---|
| 1 | `lista = datos.copy()` | c₁ | 1 |
| 2 | `comparaciones = 0` | c₂ | 1 |
| 3 | `for i in range(1, len(lista)):` | c₃ | n |
| 4 | `clave = lista[i]` | c₄ | n − 1 |
| 5 | `j = i - 1` | c₅ | n − 1 |
| 6 | `while j >= 0:` | c₆ | Σ (c_i + 1) |
| 7 | `comparaciones += 1` | c₇ | Σ c_i |
| 8 | `if lista[j] < clave:` | c₈ | Σ c_i |
| 9-10 | mover elemento y decrementar j | c₉ | Σ (c_i − [rompe antes de mover]) |
| 11 | `lista[j + 1] = clave` | c₁₁ | n − 1 |
| 12 | `return lista, comparaciones` | c₁₂ | 1 |

Las sumatorias van de i = 1 a n − 1. Agrupando lo que no depende de la forma de la entrada en constantes A y B, el costo total queda dominado por Σc_i, el total de comparaciones entre elementos:

```
T(n) = A·n + B + (c7 + c8)·Σ c_i
```

- **Mejor caso** (lista ya de mayor a menor): cada elemento nuevo se compara una sola vez con su vecino izquierdo y se detiene ahí, así que c_i = 1 para toda iteración. Σc_i = n − 1, y T(n) queda como un polinomio de grado 1: **Θ(n)**. Lo comprobé pasándole a `insertion_sort` una lista de 100 elementos ya ordenada de mayor a menor: devolvió exactamente 99 comparaciones.
- **Peor caso** (lista de menor a mayor): cada clave debe recorrer todo lo ya ordenado, c_i = i. Σc_i = n(n−1)/2, término dominante n²/2: **Θ(n²)**. Coincide con lo medido en el escenario C (ver 3.2): exactamente n(n−1)/2.
- **Caso promedio** (permutaciones equiprobables): cada clave recorre en promedio la mitad de lo ya ordenado, c_i ≈ i/2. Σc_i ≈ n(n−1)/4, sigue siendo un polinomio de grado 2: **Θ(n²)**, con la mitad de la constante del peor caso. Coincide con lo medido en el escenario A.

**Tabla de complejidades esperadas:**

| Algoritmo | Mejor caso | Caso promedio | Peor caso |
|---|---|---|---|
| Insertion sort | Θ(n) | Θ(n²) | O(n²) |
| Merge sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |

Merge sort tiene la misma cota en las tres columnas porque parte la lista por la mitad sin mirar los valores que contiene: la forma del árbol de recursión no cambia según la entrada. Insertion sort decide cuánto trabaja según lo que encuentra en cada paso, y por eso su costo se mueve entre Θ(n) y Θ(n²) dependiendo de qué tan ordenada llegue la entrada.

### 4.2 — Validación experimental

Los dos algoritmos sobre el escenario A (aleatorio), mismos tamaños de la Parte 3, mediana de tres corridas:

| n | Insertion sort — tiempo (ms) | Merge sort — tiempo (ms) |
|---|---|---|
| 100 | 0,13 | 0,11 |
| 200 | 0,49 | 0,23 |
| 400 | 1,89 | 0,51 |
| 800 | 11,97 | 1,08 |
| 1.600 | 35,05 | 2,35 |
| 3.200 | 138,35 | 4,98 |
| 6.400 | 583,82 | 10,69 |

![Tiempo de ejecución de insertion sort y merge sort frente al tamaño de entrada, escenario A](graficas/parte4_tiempo.png)

**Cuál algoritmo es mejor para Tamiza, leído en la gráfica.** Merge sort. Su curva se mantiene casi plana pegada al eje horizontal, mientras que la de insertion sort se despega con claridad a partir de n = 800 y se dispara. En n = 6.400, insertion sort tarda 583,82 ms contra 10,69 ms de merge sort: **54,6 veces más lento en el mismo punto**.

Lo que hace cada curva se ve mejor en los saltos al duplicar n: de 3.200 a 6.400, el tiempo de insertion sort se multiplica por 4,22 (138,35 → 583,82), mientras que el de merge sort se multiplica por apenas 2,15 (4,98 → 10,69).

**Coincide con lo calculado en 4.1.** El factor ≈4 al duplicar n es la firma de Θ(n²): si T(n) ≈ k·n², entonces T(2n) = 4·k·n². El factor ≈2,15 de merge sort es la firma de Θ(n log n): el crecimiento teórico esperado al duplicar n es 2 × log₂(6.400)/log₂(3.200) = 2 × 1,086 ≈ 2,17, casi idéntico al 2,15 medido.

**Qué pasa en tamaños pequeños.** Dentro del rango pedido (n = 100 a 6.400), merge sort ya es más rápido en todos los puntos medidos, incluido n = 100 (0,11 ms contra 0,13 ms). Pero medí también tamaños más pequeños, fuera de este rango, y ahí sí aparece el cruce que se espera teóricamente: en n = 20, insertion sort tardó 0,012 ms contra 0,029 ms de merge sort, y en n = 50, 0,060 ms contra 0,076 ms — insertion sort es más rápido en ambos casos. El cruce ocurre en algún punto entre n = 50 y n = 100, cuando el costo fijo de las llamadas recursivas y la creación de listas nuevas de merge sort deja de compensarse con su ventaja asintótica. Para el n real de Tamiza (1.200.000), estamos muy por encima de ese cruce, así que no aplica.

### 4.3 — Concepto técnico a la Secretaría de Salud

**Para:** equipo de ingeniería de la Secretaría de Salud
**Asunto:** algoritmo de ordenamiento del proceso nocturno de Tamiza

Mi recomendación es reemplazar insertion sort por **merge sort** como única implementación del proceso nocturno. El criterio con el que resolví el compromiso de "una sola implementación, sin importar el canal de entrada" es elegir el algoritmo por su comportamiento en el peor caso, no por el escenario más frecuente hoy: merge sort divide la lista por la mitad sin mirar los valores, así que su costo es Θ(n log n) sin importar si el lote llega aleatorio, casi ordenado o invertido. Insertion sort no ofrece esa garantía — en mis propias mediciones (n = 6.400), el mismo algoritmo tarda 0,74 ms con el lote casi ordenado y 1.166,72 ms con el lote invertido: casi 1.600 veces de diferencia decidida enteramente por cómo llegó el archivo ese día, algo que el equipo no controla.

**Estimación para la ventana de cuatro horas.** Lo siguiente es una **estimación**, no una medición: el tamaño más grande que probé fue n = 6.400, y de ahí extrapolo usando la forma de cada curva, no una regla de tres. De 6.400 a 1.200.000 el tamaño se multiplica por 187,5. Insertion sort es Θ(n²), así que su tiempo se multiplica aproximadamente por 187,5² ≈ 35.156: los 583,82 ms medidos en el escenario aleatorio se convierten en unas **5 horas y 42 minutos**, y los 1.166,72 ms del escenario invertido en unas **11 horas y 24 minutos** — ambos por fuera de la ventana, coherente con las tres madrugadas en que la lista quedó incompleta. Merge sort es Θ(n log n), así que su factor de crecimiento es 187,5 × (log₂1.200.000 / log₂6.400) ≈ 187,5 × 1,60 ≈ 300: los 10,69 ms medidos se convierten en apenas unos **3 segundos**, muy por debajo del límite.

**Sobre la propuesta de comprar el servidor del doble de velocidad.** Un servidor del doble de velocidad divide el tiempo entre dos, en el mejor de los casos, pero la brecha que hay que cerrar es de 54,6 veces — el dato que medí en n = 6.400 sobre el escenario aleatorio (gráfica `parte4_tiempo.png`: 583,82 ms de insertion sort contra 10,69 ms de merge sort). Con la máquina nueva, la estimación del proceso actual bajaría de 5 h 42 min a unas 2 h 51 min en el escenario típico —entraría en la ventana por ahora— pero seguiría sin caber en el escenario de orden inverso (11 h 24 min → 5 h 42 min, todavía por fuera). Y ese alivio se agota apenas el lote vuelva a crecer, porque el trabajo sube con el cuadrado del tamaño y el hardware solo aporta un factor fijo. Cambiar de algoritmo no tiene costo de infraestructura y deja margen para varios años de crecimiento del programa; comprar hardware más rápido pospone el problema sin resolverlo.

**Una consideración distinta del tiempo.** Merge sort necesita memoria adicional porque crea listas nuevas en cada nivel de la recursión. Lo medí con `tracemalloc` sobre n = 6.400: el pico de memoria adicional fue de unos 50 KB para insertion sort (que ordena en el mismo arreglo) contra unos 205 KB para merge sort — unas 4 veces más, aunque en términos absolutos sigue siendo un costo pequeño frente a las horas de CPU que ahorra. También vale la pena anotar que si el flujo de reproceso cambia (por ejemplo, si dejan de reenviar la lista del día anterior como base), el escenario B deja de ser "casi ordenado" y el argumento de que insertion sort "funciona bien casi siempre" se cae todavía más rápido; merge sort no depende de que ese supuesto se mantenga.
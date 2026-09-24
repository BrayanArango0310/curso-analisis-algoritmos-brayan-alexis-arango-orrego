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

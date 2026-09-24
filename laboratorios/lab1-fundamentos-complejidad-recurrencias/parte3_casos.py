"""Experimento de la Parte 3: peor, mejor y caso promedio de insertion sort."""

import time
from statistics import median

import matplotlib.pyplot as plt

from algoritmos import insertion_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso

TAMANIOS = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICIONES = 3
SEMILLA = 42

ESCENARIOS = [
    ("A - Aleatorio", generar_aleatorio),
    ("B - Casi ordenado", generar_casi_ordenado),
    ("C - Orden inverso", generar_inverso),
]


def generar_lote(generador, n: int) -> list[int]:
    """Construye el lote de un escenario respetando la firma del generador."""
    if generador is generar_inverso:
        return generador(n)
    return generador(n, SEMILLA)


def medir(lote: list[int]) -> tuple[float, int]:
    """Mide el tiempo mediano y las comparaciones de insertion_sort."""
    tiempos = []
    comparaciones = 0
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        _, comparaciones = insertion_sort(lote)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)
    return median(tiempos), comparaciones


def correr_experimento() -> dict:
    """Ejecuta la medicion de los tres escenarios en todos los tamanos."""
    resultados = {}
    for nombre, generador in ESCENARIOS:
        tiempos, comparaciones = [], []
        for n in TAMANIOS:
            lote = generar_lote(generador, n)
            tiempo, comps = medir(lote)
            tiempos.append(tiempo)
            comparaciones.append(comps)
            print(f"{nombre:20s} n={n:5d} {comps:10d} comp {tiempo:8.2f} ms")
        resultados[nombre] = {"tiempo": tiempos, "comparaciones": comparaciones}
    return resultados


def graficar(resultados: dict, clave: str, titulo: str, eje_y: str, archivo: str) -> None:
    """Dibuja una metrica de los tres escenarios en los mismos ejes."""
    figura, ejes = plt.subplots(figsize=(8, 5))
    for nombre, _ in ESCENARIOS:
        ejes.plot(TAMANIOS, resultados[nombre][clave], marker="o", label=nombre)
    ejes.set_title(titulo)
    ejes.set_xlabel("Tamaño de entrada n (número de registros)")
    ejes.set_ylabel(eje_y)
    ejes.grid(True, alpha=0.4)
    ejes.legend(title="Escenario de entrada")
    figura.tight_layout()
    figura.savefig(archivo, dpi=150)
    plt.close(figura)


def main() -> None:
    """Punto de entrada del experimento de la Parte 3."""
    resultados = correr_experimento()
    graficar(resultados, "comparaciones",
             "Insertion sort: comparaciones vs. tamaño de entrada",
             "Comparaciones entre elementos (unidades)",
             "graficas/parte3_comparaciones.png")
    graficar(resultados, "tiempo",
             "Insertion sort: tiempo de ejecución vs. tamaño de entrada",
             "Tiempo de ejecución (milisegundos)",
             "graficas/parte3_tiempo.png")


if __name__ == "__main__":
    main()
"""Medicion comparativa de la Parte 4: insertion sort contra merge sort."""

import time
from statistics import median

import matplotlib.pyplot as plt

from algoritmos import insertion_sort, merge_sort
from datos import generar_aleatorio

TAMANIOS = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICIONES = 3
SEMILLA = 42

ALGORITMOS = [
    ("Insertion sort", insertion_sort),
    ("Merge sort", merge_sort),
]


def medir(algoritmo, lote: list[int]) -> float:
    """Mide el tiempo mediano de un algoritmo sobre un lote ya construido."""
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        algoritmo(lote)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)
    return median(tiempos)


def correr_experimento() -> dict:
    """Mide los dos algoritmos sobre el escenario A en todos los tamanos."""
    resultados = {}
    for nombre, algoritmo in ALGORITMOS:
        tiempos = []
        for n in TAMANIOS:
            lote = generar_aleatorio(n, SEMILLA)
            tiempo = medir(algoritmo, lote)
            tiempos.append(tiempo)
            print(f"{nombre:15s} n={n:5d} {tiempo:8.2f} ms")
        resultados[nombre] = tiempos
    return resultados


def graficar(resultados: dict, archivo: str) -> None:
    """Dibuja el tiempo de los dos algoritmos en los mismos ejes."""
    figura, ejes = plt.subplots(figsize=(8, 5))
    for nombre, _ in ALGORITMOS:
        ejes.plot(TAMANIOS, resultados[nombre], marker="o", label=nombre)
    ejes.set_title("Escenario A: tiempo de ejecución vs. tamaño de entrada")
    ejes.set_xlabel("Tamaño de entrada n (número de registros)")
    ejes.set_ylabel("Tiempo de ejecución (milisegundos)")
    ejes.grid(True, alpha=0.4)
    ejes.legend(title="Algoritmo")
    figura.tight_layout()
    figura.savefig(archivo, dpi=150)
    plt.close(figura)


def main() -> None:
    """Punto de entrada de la medicion comparativa de la Parte 4."""
    resultados = correr_experimento()
    graficar(resultados, "graficas/parte4_tiempo.png")


if __name__ == "__main__":
    main()
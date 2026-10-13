"""Mide y grafica el tiempo de las dos soluciones del subarreglo maximo.

Ejecutar desde esta carpeta con: python medicion.py
"""

import random
import statistics
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo  # noqa: E402

SEMILLA = 42
TAMANOS = [10, 50, 100, 500, 1000, 2000, 4000, 8000]
REPETICIONES = 3
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"


def crear_datos(n: int, semilla: int) -> list[int]:
    """Genera una serie reproducible de variaciones diarias.

    Args:
        n: numero de dias que tendra la lista.
        semilla: semilla del generador aleatorio.

    Returns:
        Lista de n enteros entre -100 y 100.
    """
    generador = random.Random(semilla)
    return [generador.randint(-100, 100) for _ in range(n)]


def ejecutar_dyv(valores: list[int]) -> tuple[int, int, float]:
    """Llama a divide y venceras sobre la lista completa.

    Args:
        valores: serie de variaciones diarias.

    Returns:
        La tupla (inicio, fin, suma) de la mejor racha.
    """
    return subarreglo_maximo(valores, 0, len(valores) - 1)


def cronometrar(
    funcion: Callable[[list[int]], tuple[int, int, float]],
    valores: list[int],
) -> tuple[float, float]:
    """Cronometra una funcion varias veces y devuelve la mediana.

    Solo se cronometra la llamada al algoritmo, no la generacion de datos.

    Args:
        funcion: algoritmo que recibe la serie.
        valores: serie de variaciones diarias.

    Returns:
        Una tupla (segundos, suma) con la mediana del tiempo de
        REPETICIONES corridas y la suma que devolvio el algoritmo.
    """
    muestras = []
    suma = 0.0
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        _, _, suma = funcion(valores)
        muestras.append(time.perf_counter() - t0)
    return statistics.median(muestras), suma


def ejecutar_mediciones() -> tuple[list[float], list[float]]:
    """Mide ambos algoritmos en cada tamano e imprime la tabla.

    Returns:
        Una tupla (tiempos_fb, tiempos_dyv) en milisegundos, en el mismo
        orden que TAMANOS.
    """
    tiempos_fb = []
    tiempos_dyv = []
    encabezado = "fuerza bruta (ms)"
    print(f"{'n':>6} | {encabezado:>18} | {'divide y venceras (ms)':>22}")
    print("-" * 54)
    for tamano in TAMANOS:
        serie = crear_datos(tamano, SEMILLA)
        t_fb, suma_fb = cronometrar(subarreglo_fuerza_bruta, serie)
        t_dyv, suma_dyv = cronometrar(ejecutar_dyv, serie)
        assert suma_fb == suma_dyv, f"Las sumas no coinciden en n={tamano}"
        tiempos_fb.append(t_fb * 1000)
        tiempos_dyv.append(t_dyv * 1000)
        print(f"{tamano:>6} | {t_fb * 1000:>18.3f} | {t_dyv * 1000:>22.3f}")
    return tiempos_fb, tiempos_dyv


def graficar(
    tiempos_fb: list[float], tiempos_dyv: list[float], logaritmica: bool
) -> Path:
    """Dibuja las dos curvas de tiempo en los mismos ejes.

    Args:
        tiempos_fb: milisegundos medidos para la fuerza bruta.
        tiempos_dyv: milisegundos medidos para divide y venceras.
        logaritmica: si es True usa escala logaritmica en ambos ejes.

    Returns:
        Ruta del archivo PNG generado.
    """
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(TAMANOS, tiempos_fb, marker="o", label="Fuerza bruta Θ(n²)")
    ax.plot(
        TAMANOS, tiempos_dyv, marker="s", label="Divide y vencerás Θ(n log n)"
    )
    ax.set_xlabel("Tamaño de la serie n (días)")
    ax.set_ylabel("Tiempo de ejecución (ms)")
    if logaritmica:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title("Subarreglo máximo: tiempo vs. n (escala log-log)")
        nombre = "tiempo_vs_n_log.png"
    else:
        ax.set_title(
            "Subarreglo máximo: tiempo de ejecución vs. tamaño de entrada"
        )
        nombre = "tiempo_vs_n.png"
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    ruta = CARPETA_GRAFICAS / nombre
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def main() -> None:
    """Ejecuta el experimento y genera las dos graficas."""
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    tiempos_fb, tiempos_dyv = ejecutar_mediciones()
    for logaritmica in (False, True):
        ruta = graficar(tiempos_fb, tiempos_dyv, logaritmica)
        print(f"Gráfica guardada en {ruta}")


if __name__ == "__main__":
    main()

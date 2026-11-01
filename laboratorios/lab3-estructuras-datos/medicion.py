"""Experimentos A y B del Laboratorio 3: lista enlazada contra tabla hash.

Ejecutar desde esta carpeta con: python medicion.py
"""

import random
import statistics
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from estructuras import ListaEnlazada, TablaHash  # noqa: E402

SEMILLA_COLECCION = 2026
CONSULTAS = 200
RONDAS = 15
TAMANO_MUESTRA = 40
VALORES_N = [100, 250, 500, 1000, 2500, 5000, 10000, 20000, 40000]
N_FIJO = 20000
VALORES_ALFA = [0.25, 0.5, 1, 2, 4, 7, 10]
ESTADOS = ["en bodega", "en reparto", "entregado", "devuelto"]
CARPETA = Path(__file__).parent / "graficas"


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def crear_envios(n: int) -> list[tuple[int, str]]:
    """Arma una coleccion reproducible de envios con guias distintas.

    Args:
        n: numero de envios de la coleccion.

    Returns:
        Lista de n pares (guia, estado) con guias de diez digitos.
    """
    azar = random.Random(SEMILLA_COLECCION)
    usadas: set[int] = set()
    envios: list[tuple[int, str]] = []
    while len(envios) < n:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in usadas:
            usadas.add(guia)
            envios.append((guia, azar.choice(ESTADOS)))
    return envios


def siguiente_primo(desde: int) -> int:
    """Devuelve el menor numero primo mayor o igual a `desde`.

    Args:
        desde: valor a partir del cual se busca el primo.

    Returns:
        El primer primo que aparece contando hacia arriba desde `desde`.
    """
    candidato = max(2, desde)
    while True:
        divisor = 2
        es_primo = True
        while divisor * divisor <= candidato:
            if candidato % divisor == 0:
                es_primo = False
                break
            divisor += 1
        if es_primo:
            return candidato
        candidato += 1


def llenar_tabla(envios: list[tuple[int, str]], m: int) -> TablaHash:
    """Crea una tabla hash de m casillas con todos los envios.

    Args:
        envios: pares (guia, estado) a guardar.
        m: numero de casillas.

    Returns:
        La tabla ya cargada.
    """
    tabla = TablaHash(m)
    for guia, estado in envios:
        tabla.insertar(guia, estado)
    return tabla


def llenar_lista(envios: list[tuple[int, str]]) -> ListaEnlazada:
    """Crea una lista enlazada con todos los envios.

    Args:
        envios: pares (guia, estado) a guardar.

    Returns:
        La lista ya cargada.
    """
    lista = ListaEnlazada()
    for guia, estado in envios:
        lista.insertar(guia, estado)
    return lista


def comprobar_muestra(
    lista: ListaEnlazada, tabla: TablaHash, envios: list[tuple[int, str]]
) -> None:
    """Verifica que lista y tabla den el mismo estado en guias existentes.

    Args:
        lista: lista enlazada cargada.
        tabla: tabla hash cargada con los mismos envios.
        envios: pares (guia, estado) guardados en ambas.
    """
    azar = random.Random(99)
    for guia, estado in azar.sample(envios, min(TAMANO_MUESTRA, len(envios))):
        assert lista.buscar(guia) == tabla.buscar(guia) == estado, guia


def tiempo_por_consulta(
    estructura: ListaEnlazada | TablaHash, guias: list[int]
) -> float:
    """Mide el tiempo medio de una busqueda, en microsegundos.

    Solo el ciclo de busquedas queda dentro del cronometro. Se repite
    RONDAS veces y se toma la mediana para reducir el ruido.

    Args:
        estructura: lista o tabla ya construida.
        guias: guias a consultar (todas inexistentes).

    Returns:
        Mediana del tiempo medio por busqueda, en microsegundos.
    """
    medias = []
    for _ in range(RONDAS):
        t0 = time.perf_counter()
        for guia in guias:
            estructura.buscar(guia)
        transcurrido = time.perf_counter() - t0
        medias.append(transcurrido / len(guias) * 1_000_000)
    return statistics.median(medias)


def experimento_a() -> tuple[list[float], list[float]]:
    """Compara lista y tabla con alfa cercano a 2 para cada valor de n.

    Returns:
        Una tupla (tiempos_lista, tiempos_tabla) en microsegundos, en el
        mismo orden que VALORES_N.
    """
    print("Experimento A: busquedas de guias inexistentes")
    print(f"{'n':>7} {'m':>7} {'alfa':>6} {'lista (us)':>12} "
          f"{'tabla (us)':>11}")
    t_lista: list[float] = []
    t_tabla: list[float] = []
    for n in VALORES_N:
        envios = crear_envios(n)
        m = siguiente_primo(n // 2)
        lista = llenar_lista(envios)
        tabla = llenar_tabla(envios, m)
        comprobar_muestra(lista, tabla, envios)
        guardadas = {guia for guia, _ in envios}
        consultas = generar_guias_inexistentes(guardadas, CONSULTAS)
        t_lista.append(tiempo_por_consulta(lista, consultas))
        t_tabla.append(tiempo_por_consulta(tabla, consultas))
        print(f"{n:>7} {m:>7} {tabla.factor_carga():>6.2f} "
              f"{t_lista[-1]:>12.3f} {t_tabla[-1]:>11.3f}")
    return t_lista, t_tabla


def experimento_b() -> tuple[list[float], list[float]]:
    """Mide la tabla con n fijo y distintos factores de carga.

    Returns:
        Una tupla (alfas_reales, tiempos) con los tiempos en
        microsegundos.
    """
    print(f"\nExperimento B: tabla hash con n = {N_FIJO}")
    print(f"{'m':>7} {'alfa':>6} {'tabla (us)':>11}")
    envios = crear_envios(N_FIJO)
    guardadas = {guia for guia, _ in envios}
    consultas = generar_guias_inexistentes(guardadas, CONSULTAS)
    alfas: list[float] = []
    tiempos: list[float] = []
    for objetivo in VALORES_ALFA:
        m = siguiente_primo(round(N_FIJO / objetivo))
        tabla = llenar_tabla(envios, m)
        alfas.append(tabla.factor_carga())
        tiempos.append(tiempo_por_consulta(tabla, consultas))
        print(f"{m:>7} {alfas[-1]:>6.2f} {tiempos[-1]:>11.3f}")
    return alfas, tiempos


def graficar_a(
    t_lista: list[float], t_tabla: list[float], logaritmica: bool
) -> Path:
    """Dibuja el experimento A con las dos curvas en los mismos ejes.

    Args:
        t_lista: tiempos de la lista en microsegundos.
        t_tabla: tiempos de la tabla en microsegundos.
        logaritmica: si es True usa escala logaritmica en ambos ejes.

    Returns:
        Ruta del PNG generado.
    """
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(VALORES_N, t_lista, marker="o", label="Lista enlazada")
    ax.plot(VALORES_N, t_tabla, marker="s", label="Tabla hash (α ≈ 2)")
    ax.set_xlabel("Número de guías almacenadas n")
    ax.set_ylabel("Tiempo medio por búsqueda (µs)")
    if logaritmica:
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title("Guía inexistente: lista vs. tabla (escala log-log)")
        nombre = "lista_vs_tabla_log.png"
    else:
        ax.set_title("Guía inexistente: tiempo medio de búsqueda vs. n")
        nombre = "lista_vs_tabla.png"
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    ruta = CARPETA / nombre
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def graficar_b(alfas: list[float], tiempos: list[float]) -> Path:
    """Dibuja el tiempo de la tabla frente al factor de carga.

    Args:
        alfas: factores de carga reales de cada tabla.
        tiempos: tiempos medios por busqueda en microsegundos.

    Returns:
        Ruta del PNG generado.
    """
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.plot(alfas, tiempos, marker="D", color="tab:orange",
            label=f"Tabla hash, n = {N_FIJO} guías")
    ax.set_xlabel("Factor de carga α = n / m (guías por casilla)")
    ax.set_ylabel("Tiempo medio por búsqueda (µs)")
    ax.set_title("Guía inexistente: tiempo medio de búsqueda vs. α")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    ruta = CARPETA / "tiempo_vs_alfa.png"
    fig.savefig(ruta, dpi=150)
    plt.close(fig)
    return ruta


def main() -> None:
    """Corre los dos experimentos y guarda las tres graficas."""
    CARPETA.mkdir(exist_ok=True)
    t_lista, t_tabla = experimento_a()
    alfas, tiempos = experimento_b()
    print()
    for ruta in (graficar_a(t_lista, t_tabla, False),
                 graficar_a(t_lista, t_tabla, True),
                 graficar_b(alfas, tiempos)):
        print(f"Gráfica guardada en {ruta}")


if __name__ == "__main__":
    main()

"""Pruebas de la lista enlazada y la tabla hash del Laboratorio 3.

Ejecutar desde esta carpeta con: python pruebas.py
"""

import random

from estructuras import ListaEnlazada, TablaHash

SERIE_EJEMPLO = [
    (1000000010, "en bodega"),
    (1000000024, "en reparto"),
    (1000000017, "en bodega"),
    (1000000005, "entregado"),
]
ESTADOS = ["en bodega", "en reparto", "entregado", "devuelto"]


def cargar(envios, m):
    """Devuelve una lista y una tabla con los mismos envios."""
    lista = ListaEnlazada()
    tabla = TablaHash(m)
    for guia, estado in envios:
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)
    return lista, tabla


def longitudes(tabla):
    """Cuenta, recorriendo los nodos, cuantas guias hay en cada casilla."""
    conteo = []
    for casilla in tabla.casillas:
        total = 0
        nodo = casilla.cabeza
        while nodo is not None:
            total += 1
            nodo = nodo.siguiente
        conteo.append(total)
    return conteo


# --- 1. Serie de ejemplo de la guia: busquedas exitosas e infructuosas ---
lista, tabla = cargar(SERIE_EJEMPLO, 11)
for guia, estado in SERIE_EJEMPLO:
    assert lista.buscar(guia) == estado
    assert tabla.buscar(guia) == estado
# Una guia mal digitada (cambia el ultimo digito) y una muy lejana.
for guia in (1000000011, 9876543210):
    assert lista.buscar(guia) is None
    assert tabla.buscar(guia) is None
assert lista.tamano == tabla.tamano == 4

# La insercion es al inicio: la ultima guia agregada queda en la cabeza.
assert lista.cabeza.guia == 1000000005
assert lista.cabeza.siguiente.guia == 1000000017

# --- 2. Colision forzada de la guia: m = 7 con las guias 10, 24 y 17 ---
tabla7 = TablaHash(7)
for guia in (10, 24, 17):
    assert tabla7.hash(guia) == 3
    tabla7.insertar(guia, "en bodega")
for guia in (10, 24, 17):
    assert tabla7.buscar(guia) == "en bodega"
assert tabla7.casillas[3].tamano == 3
assert longitudes(tabla7) == [0, 0, 0, 3, 0, 0, 0]
# 31 tambien cae en la casilla 3 pero no se inserto: debe dar None
# aunque se recorra una casilla con tres nodos.
assert tabla7.buscar(31) is None

# --- 3. Factor de carga tras esas tres inserciones ---
assert tabla7.factor_carga() == 3 / 7

# --- 3b. Las guias reales del ejemplo tambien chocan con m = 7 ---
# 1000000010, 1000000024 y 1000000017 dan residuo 2; 1000000005 da 4.
_, tabla_real = cargar(SERIE_EJEMPLO, 7)
assert longitudes(tabla_real) == [0, 0, 3, 0, 1, 0, 0]
assert tabla_real.buscar(1000000024) == "en reparto"
assert tabla_real.factor_carga() == 4 / 7

# --- 4. Colecciones aleatorias: lista y tabla deben responder igual ---
azar = random.Random(31)
for ronda in range(25):
    cantidad = azar.randint(1, 400)
    # Se alternan m pequenos (muchas colisiones) y m grandes (pocas).
    m = azar.choice([1, 2, 5, 13, 97, 401])
    usadas = set()
    envios = []
    while len(envios) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in usadas:
            usadas.add(guia)
            envios.append((guia, azar.choice(ESTADOS)))
    lista, tabla = cargar(envios, m)

    for guia, estado in envios:
        assert lista.buscar(guia) == tabla.buscar(guia) == estado

    revisadas = 0
    while revisadas < 30:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia in usadas:
            continue
        assert lista.buscar(guia) is None
        assert tabla.buscar(guia) is None
        revisadas += 1

    assert sum(longitudes(tabla)) == tabla.tamano == cantidad
    assert tabla.factor_carga() == cantidad / m

# --- 5. Casos limite ---
vacia = ListaEnlazada()
assert vacia.buscar(1000000010) is None
assert TablaHash(5).buscar(1000000010) is None
assert TablaHash(5).factor_carga() == 0

print("Todas las pruebas pasaron.")

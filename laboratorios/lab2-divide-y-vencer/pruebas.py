"""Pruebas de las dos soluciones del subarreglo maximo.

Ejecutar desde esta carpeta con: python pruebas.py
"""

import random

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo, suma_cruzada


def dyv(valores):
    return subarreglo_maximo(valores, 0, len(valores) - 1)


def revisar(valores, suma_esperada):
    """Compara la suma de ambas soluciones contra la esperada."""
    copia = list(valores)
    for resultado in (subarreglo_fuerza_bruta(valores), dyv(valores)):
        inicio, fin, suma = resultado
        assert suma == suma_esperada, (valores, resultado, suma_esperada)
        # Los indices devueltos deben sumar lo que dice el algoritmo.
        assert sum(valores[inicio:fin + 1]) == suma, (valores, resultado)
    # Ninguna funcion debe modificar la lista recibida.
    assert valores == copia


# 1. Serie de ocho dias de la situacion problema: dias 2 a 7, suma 17.
revisar([-3, 5, -2, 8, -6, 3, 9, -4], 17)

# 2. Un solo elemento (positivo y negativo).
revisar([7], 7)
revisar([-4], -4)

# 3. Todos negativos: la mejor racha es el dia menos malo.
revisar([-8, -3, -6, -2, -5], -2)

# 4. Todos positivos: la mejor racha es la serie completa.
revisar([4, 1, 6, 2, 3], 16)

# 5. El mejor tramo cruza el punto medio (medio = indice 2).
#    Izquierda sola da 5, derecha sola da 6, el cruzado da 1 + 4 + 6 = 11.
serie_cruzada = [-9, 1, 4, 6, -9]
revisar(serie_cruzada, 11)
assert dyv(serie_cruzada)[:2] == (1, 3)

# 5b. suma_cruzada probada directamente.
#     Serie de ocho dias con medio = 3: tramo de los indices 1 a 6, suma 17.
assert suma_cruzada([-3, 5, -2, 8, -6, 3, 9, -4], 0, 3, 7) == (1, 6, 17)
assert suma_cruzada(serie_cruzada, 0, 2, 4) == (1, 3, 11)

# 6. Veinte listas aleatorias (semilla fija): ambas sumas deben coincidir.
generador = random.Random(2026)
for _ in range(20):
    largo = generador.randint(1, 60)
    lista = [generador.randint(-100, 100) for _ in range(largo)]
    esperada = subarreglo_fuerza_bruta(lista)[2]
    revisar(lista, esperada)

print("Todas las pruebas pasaron.")

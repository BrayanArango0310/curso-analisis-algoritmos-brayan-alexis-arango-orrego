"""Subarreglo maximo: fuerza bruta y divide y venceras."""


def subarreglo_fuerza_bruta(valores: list[float]) -> tuple[int, int, float]:
    """Encuentra la mejor racha probando todos los pares de dias (i, j).

    Args:
        valores: variacion diaria de caja, una por dia. Tiene al menos
            un elemento.

    Returns:
        Una tupla (inicio, fin, suma) con los indices inclusivos del
        tramo de mayor suma y el valor de esa suma.
    """
    n = len(valores)
    desde = 0
    hasta = 0
    record = valores[0]
    for i in range(n):
        acumulado = 0
        for j in range(i, n):
            acumulado += valores[j]
            if acumulado > record:
                record = acumulado
                desde = i
                hasta = j
    return desde, hasta, record


def suma_cruzada(
    valores: list[float], inicio: int, medio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra el mejor tramo que cruza el punto medio.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango considerado (inclusive).
        medio: indice del ultimo elemento de la mitad izquierda.
        fin: indice final del rango considerado (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo que incluye al
        menos un elemento de cada mitad.
    """
    # Barrido hacia la izquierda: arranca en medio y retrocede.
    suma_izq = valores[medio]
    acumulado = 0
    corte_izq = medio
    for i in range(medio, inicio - 1, -1):
        acumulado += valores[i]
        if acumulado > suma_izq:
            suma_izq = acumulado
            corte_izq = i

    # Barrido hacia la derecha: arranca en medio + 1 y avanza.
    suma_der = valores[medio + 1]
    acumulado = 0
    corte_der = medio + 1
    for j in range(medio + 1, fin + 1):
        acumulado += valores[j]
        if acumulado > suma_der:
            suma_der = acumulado
            corte_der = j

    return corte_izq, corte_der, suma_izq + suma_der


def subarreglo_maximo(
    valores: list[float], inicio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra la mejor racha por divide y venceras.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango a considerar (inclusive).
        fin: indice final del rango a considerar (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo dentro de
        valores[inicio..fin].
    """
    if inicio == fin:
        return inicio, fin, valores[inicio]

    medio = (inicio + fin) // 2
    izquierdo = subarreglo_maximo(valores, inicio, medio)
    derecho = subarreglo_maximo(valores, medio + 1, fin)
    cruzado = suma_cruzada(valores, inicio, medio, fin)

    mejor = izquierdo
    if derecho[2] > mejor[2]:
        mejor = derecho
    if cruzado[2] > mejor[2]:
        mejor = cruzado
    return mejor

"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Fuerza bruta

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""

import itertools
import string
import time

# ---------------------------------------------------------------------------
# Alfabetos predefinidos
# ---------------------------------------------------------------------------
DIGITOS    = string.digits                      # '0123456789'
MINUSCULAS = string.ascii_lowercase             # 'abcdefghijklmnopqrstuvwxyz'
ALNUM      = string.ascii_letters + string.digits


# ---------------------------------------------------------------------------
# Problema A – Generación y búsqueda exhaustiva
# ---------------------------------------------------------------------------

def generar_candidatos(alfabeto: str, longitud: int):
    """
    Genera (como iterador) todas las cadenas de exactamente 'longitud'
    caracteres del alfabeto dado.

    Pistas:
        itertools.product(alfabeto, repeat=longitud) produce tuplas de caracteres.
        "".join(tupla) convierte una tupla en cadena.
    """
    # TODO: implementa con itertools.product y yield o return del iterador
    for tupla in itertools.product(alfabeto, repeat=longitud):
        yield "".join(tupla)



def buscar_cadena_objetivo(objetivo: str, alfabeto: str,
                           min_len: int = 1) -> tuple:
    """
    Busca 'objetivo' recorriendo todas las cadenas del alfabeto de longitud
    min_len hasta len(objetivo) (inclusive).

    Retorna:
        (encontrada: bool, intentos: int, tiempo_seg: float)
    """
    intentos = 0
    inicio   = time.perf_counter()

    for longitud in range(min_len, len(objetivo) + 1):
        for candidato in generar_candidatos(alfabeto, longitud):
            # TODO: incrementa intentos
            intentos+=1
            # TODO: si candidato == objetivo, calcula el tiempo y retorna
            #       (True, intentos, tiempo)
            if candidato==objetivo:
                tiempo=time.perf_counter()-inicio
                return(True,intentos,tiempo)


    tiempo = time.perf_counter() - inicio
    return (False,intentos,tiempo)


# ---------------------------------------------------------------------------
# Problema B – Análisis de crecimiento
# ---------------------------------------------------------------------------

def combinar_teoricas(alfabeto: str, min_len: int, max_len: int) -> int:
    """
    Calcula el número teórico de cadenas a explorar.

    Fórmula: suma de |alfabeto|^k  para k en [min_len, max_len]

    Pistas:
        sum(expr for k in range(...)) es la forma idiomática.
        len(alfabeto) da |Σ|.
    """
    # TODO: implementa la fórmula
    sigma=len(alfabeto)
    return sum(sigma**k for k in range(min_len, max_len +1))


# ---------------------------------------------------------------------------
# Problema C – Optimización con poda por prefijo
# ---------------------------------------------------------------------------

def buscar_con_poda(objetivo: str, alfabeto: str,
                    prefijos_validos: set) -> tuple:
    """
    Variante con poda: antes de contar un candidato, verifica que cada uno
    de sus prefijos propios esté en 'prefijos_validos'.  Si algún prefijo
    falta, descarta la rama completa (usa continue).

    Retorna:
        (encontrada: bool, intentos: int, tiempo_seg: float)

    Pistas:
        El prefijo de longitud k de 'cadena' es candidato[:k].
        Prueba prefijos para k en range(1, len(candidato)).
    """
    intentos = 0
    inicio   = time.perf_counter()

    for longitud in range(1, len(objetivo) + 1):
        for partes in itertools.product(alfabeto, repeat=longitud):
            candidato = "".join(partes)

            # TODO: verifica los prefijos; si alguno no está en
            #       prefijos_validos, usa 'continue' para saltar.
            valido=True
            for k in range(1,len(candidato)):
                if candidato[:k] not in prefijos_validos:
                    valido=False
                    break
            if not valido:
                continue
            # TODO: incrementa intentos y compara con objetivo.
            intentos+=1
            if candidato==objetivo:
                tiempo=time.perf_counter()-inicio
                return(True,intentos,tiempo)

    tiempo = time.perf_counter() - inicio
    return (False, intentos, tiempo)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    objetivo = "Sl2"
    print("=== Búsqueda por fuerza bruta ===")
    encontrada, intentos, t = buscar_cadena_objetivo(objetivo, ALNUM)
    if encontrada:
        print(f"  Objetivo : '{objetivo}'")
        print(f"  Intentos : {intentos}")
        print(f"  Tiempo   : {t:.4f} s")
        print(f"  Tasa     : {intentos / t:.0f} candidatos/s")
    else:
        print("  generar_candidatos aún no implementada (o target no encontrado)")

    print("\n=== Combinaciones teóricas ===")
    for max_len in [3, 4]:
        n = combinar_teoricas(ALNUM, 1, max_len)
        if n is not None:
            print(f"  ALNUM (A-Z, a-z, 0-9) hasta longitud {max_len}: {n:,} candidatos")
        else:
            print("  combinar_teoricas aún no implementada")
        break
#------------
print("=== Problema B ===")

for alfabeto, nombre in [(DIGITOS, "Dígitos"), (MINUSCULAS, "Minúsculas")]:
    for n in [3, 4, 5]:
        teoricas = combinar_teoricas(alfabeto, 1, n)

        objetivo = alfabeto[-1] * n   # peor caso
        encontrada, intentos, t = buscar_cadena_objetivo(objetivo, alfabeto)

        print(nombre, n, teoricas, f"{t:.4f}s")
#-------------
print("=== Problema C ===")
objetivo = "datos"
alfabeto = MINUSCULAS
prefijos = {"d", "da", "dat", "dato"}
# Sin poda
_, intentos1, t1 = buscar_cadena_objetivo(objetivo, alfabeto)
# Con poda
_, intentos2, t2 = buscar_con_poda(objetivo, alfabeto, prefijos)
reduccion = ((t1 - t2) / t1) * 100
print("Objetivo: datos")
print("Prefijos: 'd','da','dat','dato'")
print(f"Sin poda: {t1:.4f}s")
print(f"Con poda: {t2:.4f}s")
print(f"Intentos sin poda: {intentos1}")
print(f"Intentos con poda: {intentos2}")
print(f"Reducción %: {reduccion:.2f}%")
#-----------
print("=== Problema D.1 ===")
prev = None
for n in range(1, 6):
    objetivo = "9" * n
    _, intentos, t = buscar_cadena_objetivo(objetivo, DIGITOS)
    razon = t / prev if prev else None
    if razon is None:
        print(n, intentos, f"{t:.4f}s", "—")
    else:
        print(n, intentos, f"{t:.4f}s", f"{razon:.2f}")
    prev = t

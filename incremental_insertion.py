"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Estrategia incremental – Insertion sort instrumentado

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""

import time
import random


# ---------------------------------------------------------------------------
# Problema A – Insertion sort con métricas
# ---------------------------------------------------------------------------

def insertion_sort_metricas(arr: list) -> tuple:
    """
    Ordena 'arr' usando insertion sort e instrumenta la ejecución.

    Retorna:
        (arreglo_ordenado, comparaciones, movimientos, tiempo_seg)

    Pistas:
        El bucle externo recorre i de 1 a n-1.
        'llave' = arr[i] es el elemento a insertar.
        El bucle interno (while) desplaza elementos mayores que 'llave' hacia
        la derecha; cada desplazamiento es un movimiento.
        Cuenta también la última comparación del while (la que falla).
        La colocación final de llave es un movimiento.
    """
    arr          = arr.copy()
    n            = len(arr)
    comparaciones = 0
    movimientos   = 0
    inicio        = time.perf_counter()

    for i in range(1, n):
        llave = arr[i]
        j = i - 1
        
        # TODO: mientras j >= 0 y arr[j] > llave:
        #           - incrementa comparaciones
        #           - desplaza arr[j] a arr[j+1], incrementa movimientos
        #           - decrement j
        while j>=0 and arr[j] > llave:
            comparaciones+=1
            arr[j+1]= arr[j]
            movimientos+=1
            j -= 1

        # TODO: cuenta la comparación que termina el while (si j >= 0)
        if j>=0:
           comparaciones+=1

        # TODO: coloca llave en arr[j + 1] e incrementa movimientos
        arr[j+1]=llave
        movimientos+=1
    
    tiempo = time.perf_counter() - inicio
    return (arr, comparaciones, movimientos, tiempo)


# ---------------------------------------------------------------------------
# Problema B – Generación de escenarios
# ---------------------------------------------------------------------------

def generar_arreglo(n: int, escenario: str) -> list:
    """
    Genera un arreglo de tamaño n según el escenario indicado.

    Escenarios:
        'mejor'    -> ya ordenado de menor a mayor    (mejor caso: Θ(n))
        'peor'     -> inversamente ordenado            (peor caso:  Θ(n²))
        'promedio' -> aleatorio                        (caso promedio: Θ(n²))

    Pistas:
        list(range(n))           arreglo [0, 1, 2, ..., n-1]
        list(range(n, 0, -1))    arreglo [n, n-1, ..., 1]
        random.shuffle(arr)      mezcla in-place
    """
    # TODO: implementa los tres escenarios; lanza ValueError si escenario es inválido.
    if escenario=="mejor":
        return list(range(n))
    elif escenario =="peor":
        return list(range(n,0,-1))        
    elif escenario =="promedio":
        arr = list(range(n))
        random.shuffle(arr)
        return arr
    else:
        raise ValueError ("Escenario invalido")

def medir_escenarios(tamanos: list) -> list:
    """
    Para cada tamaño en 'tamanos' evalúa los tres escenarios e imprime resultados.

    Retorna:
        Lista de dicts: {tamano, escenario, comparaciones, movimientos, tiempo}
    """
    resultados = []
    for n in tamanos:
        for escenario in ("mejor", "promedio", "peor"):
            arr = generar_arreglo(n, escenario)
            # TODO: llama a insertion_sort_metricas y guarda el resultado.
            # Estructura del dict:
            # {
            #   "tamano": n,
            #   "escenario": escenario,
            #   "comparaciones": ...,
            #   "movimientos": ...,
            #   "tiempo": ...
            # }
            ordenado, comps, movs, tiempo = insertion_sort_metricas(arr) 
            resultados.append({
                "tamano":n,
                "escenario":escenario,
                "comparaciones":comps,
                "movimientos":movs,
                "tiempo":tiempo,})
                
    return resultados

# ---------------------------------------------------------------------------
# Problema D – Versión híbrida (insertion sort + merge sort)
# ---------------------------------------------------------------------------

def _merge(izq: list, der: list) -> list:
    """Combina dos listas ordenadas en una sola."""
    # TODO: implementa la fusión estándar de merge sort.
    resultado=[]
    i = j = 0
    while i<len(izq) and j< len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i+=1
        else:
            resultado.append(der[j])
            j+=1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def _merge_sort_hibrido(arr: list, umbral: int) -> list:
    """
    Divide 'arr' recursivamente.
    Si el subarreglo tiene tamaño <= umbral, usa insertion_sort_metricas.
    Si no, divide a la mitad y fusiona con _merge.
    """
    if len(arr) <= umbral:
        # TODO: retorna insertion_sort_metricas(arr)[0]
        return insertion_sort_metricas(arr)[0]
    mid = len(arr) // 2
    # TODO: llama recursivamente y fusiona con _merge
    izq= _merge_sort_hibrido(arr[:mid], umbral)
    der= _merge_sort_hibrido(arr[mid:], umbral)
    return _merge(izq, der)

def insertion_sort_hibrido(arr: list, umbral: int = 32) -> list:
    """
    Punto de entrada del ordenamiento híbrido.
    Retorna el arreglo ordenado.
    """
    # TODO: llama a _merge_sort_hibrido
    return _merge_sort_hibrido(arr, umbral)

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    tamanos = [1000, 2000, 4000, 8000]
    print("Midiendo escenarios... (puede tardar unos segundos)\n")
    resultados = medir_escenarios(tamanos)

    if resultados:
        print(f"{'Tamaño':>8} {'Escenario':>10} {'Comps':>12} "
              f"{'Movs':>12} {'Tiempo (s)':>12}")
        print("-" * 60)
        for r in resultados:
            print(f"{r['tamano']:>8} {r['escenario']:>10} "
                  f"{r['comparaciones']:>12} {r['movimientos']:>12} "
                  f"{r['tiempo']:>12.4f}")
    else:
        print("medir_escenarios aún no implementada.")

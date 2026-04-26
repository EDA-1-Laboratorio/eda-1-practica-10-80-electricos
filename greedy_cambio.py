"""
Práctica 10 – Estrategias para la construcción de algoritmos I
Módulo  : Algoritmo ávido (greedy) – Cambio de monedas

Instrucciones
    Implementa las funciones marcadas con TODO.
    Ejecuta el archivo directamente para verificar tu avance.
"""


# ---------------------------------------------------------------------------
# Problema A – Solución greedy
# ---------------------------------------------------------------------------

def cambio_greedy(monto: int, monedas: list) -> tuple | None:
    """
    Resuelve el problema de cambio con la estrategia ávida:
    en cada paso usa la moneda de mayor valor que quepa.

    Parámetros:
        monto   – Cantidad (entero positivo) a devolver.
        monedas – Lista de denominaciones disponibles (enteros positivos).

    Retorna:
        (usadas: list, total: int)  si hay solución exacta.
        None                        si el monto no se puede completar.

    Pistas:
        sorted(monedas, reverse=True) ordena de mayor a menor.
        cantidad = restante // moneda  (cuántas caben)
        restante = restante % moneda   (lo que sobra)
    """
    # TODO: 1. Ordena las monedas de mayor a menor.
    monedas_ordenadas = sorted(monedas, reverse=True)
    
    # TODO: 2. Para cada denominación, toma tantas monedas como quepan.
    usadas = []
    restante = monto
    total_monedas = 0
    
    for moneda in monedas_ordenadas:
        cantidad = restante // moneda
        if cantidad > 0:
            usadas.extend([moneda] * cantidad)
            total_monedas += cantidad
            restante = restante % moneda
    
    # TODO: 3. Si el residuo final es 0, retorna (lista_de_monedas_usadas, total).
    # TODO: 4. Si queda residuo, retorna None.
    if restante == 0:
        return (usadas, total_monedas)
    else:
        return None


# ---------------------------------------------------------------------------
# Problema B – Solución óptima por programación dinámica
# ---------------------------------------------------------------------------

def cambio_optimo_dp(monto: int, monedas: list) -> tuple | None:
    """
    Resuelve el problema de cambio de manera óptima usando
    programación dinámica (número mínimo de monedas).

    Retorna:
        (usadas: list, total: int)  con mínimo de monedas.
        None                        si no hay solución exacta.

    Pistas (bottom-up DP):
        dp[i] = mínimo de monedas para devolver exactamente i.
        Inicializa: dp[0] = 0,  dp[i] = float('inf') para i > 0.
        Transición: dp[i] = min(dp[i], dp[i - m] + 1) para cada moneda m <= i.
        Guarda padre[i] = m que produjo dp[i] para reconstruir la solución.
    """
    # TODO: crea la tabla dp y la tabla padre con longitud monto + 1.
    dp = [float('inf')] * (monto + 1)
    padre = [None] * (monto + 1)
    
    dp[0] = 0
    
    # TODO: llena la tabla recorriendo cada monto parcial de 1 a monto.
    for i in range(1, monto + 1):
        for moneda in monedas:
            if moneda <= i:
                if dp[i - moneda] + 1 < dp[i]:
                    dp[i] = dp[i - moneda] + 1
                    padre[i] = moneda
    
    # TODO: si dp[monto] es inf, retorna None.
    if dp[monto] == float('inf'):
        return None
    
    # TODO: reconstruye la lista de monedas usando padre[].
    usadas = []
    restante = monto
    while restante > 0:
        moneda = padre[restante]
        usadas.append(moneda)
        restante -= moneda
    
    return (usadas, dp[monto])


# ---------------------------------------------------------------------------
# Problema C – Comparación: contraejemplos
# ---------------------------------------------------------------------------

def comparar_estrategias(monto_max: int, monedas: list) -> dict:
    """
    Para cada monto de 1 a monto_max, compara greedy vs DP.

    Retorna un diccionario con:
        'montos_greedy_falla'     : lista de montos donde greedy devuelve None
                                    pero DP sí tiene solución.
        'montos_greedy_suboptimo' : lista de (monto, total_greedy, total_dp)
                                    donde greedy usa más monedas que DP.
    """
    # TODO: itera los montos, llama a cambio_greedy y cambio_optimo_dp.
    montos_greedy_falla = []
    montos_greedy_suboptimo = []
    
    for monto in range(1, monto_max + 1):
        resultado_greedy = cambio_greedy(monto, monedas)
        resultado_dp = cambio_optimo_dp(monto, monedas)
        
    # TODO: clasifica cada caso y acumula en las listas correspondientes.
        if resultado_dp is not None and resultado_greedy is None:
            montos_greedy_falla.append(monto)
        elif resultado_greedy is not None and resultado_dp is not None:
            total_greedy = resultado_greedy[1]
            total_dp = resultado_dp[1]
            if total_greedy > total_dp:
                montos_greedy_suboptimo.append((monto, total_greedy, total_dp))
    
    return {
        'montos_greedy_falla': montos_greedy_falla,
        'montos_greedy_suboptimo': montos_greedy_suboptimo
    }


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Sistema canónico
    canonicas = [1, 2, 5, 10, 20, 50]
    print("=== Sistema canónico [1,2,5,10,20,50] ===")
    for monto in [11, 30, 63]:
        g = cambio_greedy(monto, canonicas)
        d = cambio_optimo_dp(monto, canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    # Sistema no canónico – aquí greedy falla
    no_canonicas = [1, 3, 4]
    print("\n=== Sistema no canónico [1,3,4] ===")
    for monto in [6, 12, 15]:
        g = cambio_greedy(monto, no_canonicas)
        d = cambio_optimo_dp(monto, no_canonicas)
        print(f"  Monto {monto:>3}: greedy={g}  dp={d}")

    print("\n=== Análisis completo montos 1-60, sistema [1,3,4] ===")
    resultado = comparar_estrategias(60, no_canonicas)
    if resultado is not None:
        sub = resultado.get("montos_greedy_suboptimo", [])
        fal = resultado.get("montos_greedy_falla", [])
        print(f"  Casos subóptimos : {len(sub)}")
        print(f"  Casos con fallo  : {len(fal)}")
        if sub:
            print(f"  Primeros 5 subóptimos: {sub[:5]}")
    else:
        print("  comparar_estrategias aún no implementada")

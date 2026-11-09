"""Prueba de carga para el Hito 3: muchas peticiones a /predict al mismo tiempo.

Uso: python scripts/carga.py https://<su-servicio>.onrender.com 200 20
     (URL, número de peticiones, peticiones simultáneas)
Imprime la tasa de éxito, peticiones por segundo y latencias p50 y p95.
"""
import os
import statistics
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests

URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:8000"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 200 # peticiones en total
SIMULTANEAS = int(sys.argv[3]) if len(sys.argv) > 3 else 20 # hilos a la vez
# >>> En su proyecto: cambien este ejemplo por una entrada válida de SU modelo.
DATO = {"largo_sepalo": 5.1, "ancho_sepalo": 3.5, "largo_petalo": 1.4, "ancho_petalo": 0.2}
CABECERAS = {"x-api-key": os.getenv("API_KEY", "")} # Hito 4: llave opcional
def una_peticion(_):
    """Envía una predicción y devuelve (código HTTP, milisegundos)."""
    inicio = time.perf_counter()
    try:
        r = requests.post(f"{URL}/predict", json=DATO, headers=CABECERAS, timeout=30)
        codigo = r.status_code
    except requests.RequestException: # sin respuesta: se cuenta como error
        codigo = 0
    return codigo, (time.perf_counter() - inicio) * 1000


inicio_total = time.perf_counter()
# ThreadPoolExecutor ejecuta SIMULTANEAS peticiones al mismo tiempo
with ThreadPoolExecutor(max_workers=SIMULTANEAS) as hilos:
    resultados = list(hilos.map(una_peticion, range(N)))
total = time.perf_counter() - inicio_total


tiempos = sorted(ms for _, ms in resultados)
exitos = sum(1 for codigo, _ in resultados if codigo == 200)
p95 = tiempos[int(0.95 * len(tiempos)) - 1]
print(f"exitos={exitos}/{N} peticiones_por_s={N / total:.1f} "
      f"p50={statistics.median(tiempos):.0f} ms p95={p95:.0f} ms")
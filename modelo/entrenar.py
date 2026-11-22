"""Entrena el modelo SVM del proyecto: clasificación de patrones no lineales.

Datos sintéticos make_moons (dos "lunas" entrelazadas con ruido) y algoritmo SVM
con kernel RBF. También entrena un SVM lineal como referencia para demostrar que
el kernel no lineal es necesario.
Uso: python modelo/entrenar.py [archivo_salida]
"""
import sys
import time
import tracemalloc
from datetime import datetime, timezone

import joblib
from sklearn.datasets import make_moons
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# ---------------------------------------------------------------- Configuración
SALIDA = sys.argv[1] if len(sys.argv) > 1 else "app/modelo.joblib"
SEMILLA = 42          # misma semilla = mismo resultado (reproducible)
N_MUESTRAS = 1000     # puntos sintéticos en total
RUIDO = 0.25          # desviación estándar del ruido gaussiano

# ---------------------------------------------------------------- 1. Datos
# make_moons genera dos semicírculos entrelazados: NO se pueden separar con una recta.
X, y = make_moons(n_samples=N_MUESTRAS, noise=RUIDO, random_state=SEMILLA)
NOMBRES_CLASES = ["luna_superior", "luna_inferior"]  # clase 0 y clase 1

# 70 % entrenar / 30 % evaluar; stratify conserva la proporción de cada clase.
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, random_state=SEMILLA, stratify=y)

# ---------------------------------------------------------------- 2. Modelo
# Pipeline: escala (el SVM es sensible a la escala) y aplica SVM con kernel RBF.
# probability=True permite devolver la confianza (calibración de Platt; entrena
# un poco más lento). Se mide el tiempo y la memoria pico de Python al entrenar.
tracemalloc.start()
t0 = time.perf_counter()
modelo = make_pipeline(
    StandardScaler(),
    SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=SEMILLA))
modelo.fit(X_tr, y_tr)
segundos = time.perf_counter() - t0
_, memoria_pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

# Referencia: SVM lineal (demuestra por qué hace falta el kernel RBF).
lineal = make_pipeline(StandardScaler(), SVC(kernel="linear", random_state=SEMILLA))
lineal.fit(X_tr, y_tr)
exactitud_lineal = accuracy_score(y_te, lineal.predict(X_te))

# ---------------------------------------------------------------- 3. Evaluación
predicciones = modelo.predict(X_te)
exactitud = accuracy_score(y_te, predicciones)
f1 = f1_score(y_te, predicciones, average="macro")
print(classification_report(y_te, predicciones, target_names=NOMBRES_CLASES))
print(f"SVM lineal (referencia): exactitud={exactitud_lineal:.3f}")
print(f"Entrenamiento: {segundos:.2f} s, memoria pico Python: {memoria_pico / 1e6:.1f} MB")

# ---------------------------------------------------------------- 4. Guardar
# Muestra de 200 puntos de prueba para que la página dibuje la nube de puntos.
muestra = [[round(float(a), 3), round(float(b), 3), int(c)]
           for (a, b), c in zip(X_te[:200], y_te[:200])]

joblib.dump({
    "modelo": modelo,
    "clases": NOMBRES_CLASES,
    "exactitud": round(float(exactitud), 4),
    "f1": round(float(f1), 4),
    "exactitud_lineal": round(float(exactitud_lineal), 4),
    "muestra": muestra,
    "version": datetime.now(timezone.utc).strftime("%Y%m%d%H%M"),
}, SALIDA)
print(f"exactitud={exactitud:.3f} f1={f1:.3f} guardado en {SALIDA}")

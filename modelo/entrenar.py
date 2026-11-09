"""Entrena el modelo de ClasificaIA y lo guarda en un archivo (proyecto base).

ClasificaIA clasifica flores Iris con KNN (k vecinos más cercanos). Es el EJEMPLO
del proyecto: cada equipo cambia los datos y el algoritmo por los suyos.
Uso: python modelo/entrenar.py [archivo_salida]
"""
import sys
from datetime import datetime, timezone

import joblib
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------- Configuración
# Archivo donde se guarda el modelo; la API lo lee al iniciar.
SALIDA = sys.argv[1] if len(sys.argv) > 1 else "app/modelo.joblib"
SEMILLA = 42 # misma semilla = mismo resultado (reproducible)

# ---------------------------------------------------------------- 1. Datos
# load_iris trae 150 flores con 4 medidas (cm) y su especie (0, 1 o 2).
# >>> En su proyecto: aquí cargan SUS datos (CSV, dataset de scikit-learn, etc.).
iris = load_iris()
X, y = iris.data, iris.target
NOMBRES_CLASES = list(iris.target_names) # ["setosa", "versicolor", ...]

# 70 % para entrenar y 30 % para evaluar. stratify mantiene la proporción de
# cada clase en ambos conjuntos; el modelo nunca ve los datos de prueba.
X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, random_state=SEMILLA, stratify=y)

# ---------------------------------------------------------------- 2. Modelo
# Pipeline: primero escala las medidas (media 0, desviación 1) y luego aplica
# KNN. Escalar importa en KNN porque compara distancias entre puntos.
# >>> En su proyecto: cambian KNeighborsClassifier por su algoritmo.
modelo = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
modelo.fit(X_tr, y_tr)

# ---------------------------------------------------------------- 3. Evaluación
predicciones = modelo.predict(X_te)
exactitud = accuracy_score(y_te, predicciones) # proporción de aciertos
print(classification_report(y_te, predicciones, target_names=NOMBRES_CLASES))

# ---------------------------------------------------------------- 4. Guardar
# Se guarda un diccionario: el modelo y los datos que la API necesita mostrar.
joblib.dump({
    "modelo": modelo,
    "clases": NOMBRES_CLASES,
    "exactitud": round(float(exactitud), 4),
    "version": datetime.now(timezone.utc).strftime(" %Y %m %d %H %M"), # fecha del modelo
}, SALIDA)
print(f"exactitud={exactitud:.3f} guardado en {SALIDA}")
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import joblib

# 1. Carga de datos reales (Digits: 64 píxeles)
digits = load_digits()
X, y = digits.data, digits.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

NOMBRES_CLASES = [str(i) for i in range(10)]  # Dígitos del 0 al 9

# 2. Algoritmo SVM
modelo = make_pipeline(
    StandardScaler(),
    SVC(kernel='rbf', probability=True, random_state=42)
)
modelo.fit(X_train, y_train)

# 3. Métrica numérica obligatoria (Accuracy)
accuracy = modelo.score(X_test, y_test)
print(f"Accuracy del modelo SVM en Digits: {accuracy:.4f}")

# Guardar si es necesario
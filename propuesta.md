Proyecto CN: Clasificación de Patrones No Lineales con Datos Sintéticos (make_moons)
1. Problema
El reto consiste en entrenar un modelo de aprendizaje automático capaz de separar y clasificar correctamente dos grupos de datos que no se pueden dividir con una simple línea recta (clasificación no lineal). Este tipo de problemas simula escenarios reales donde los límites entre clases son curvos o complejos.
2. Datos
 * Origen: Se generarán datos artificiales utilizando la función make_moons de scikit-learn (un dataset sintético integrado en la librería).
 * Características: Genera puntos distribuidos en forma de dos medias lunas entrelazadas.
 * Dimensiones: Por lo general, se configuran alrededor de 1,000 muestras con un nivel de ruido controlado para hacer el desafío más realista. Cada muestra consta de 2 características (coordenadas X e Y en el plano cartesiano) y una etiqueta binaria (0 o 1) que indica a qué luna pertenece cada punto.
3. Significados
 * Variables de entrada (X): Las coordenadas bidimensionales (x_1, x_2) de cada punto en el plano.
 * Variable objetivo (y): La clase a la que pertenece el punto (Luna A o Luna B).
 * Frontera de decisión: La línea curva que el modelo SVM aprende a trazar para separar ambas formas de manera óptima.
4. Métrica Objetiva
Para evaluar el desempeño del modelo SVM, se utilizarán:
 * Exactitud (Accuracy): Porcentaje de puntos clasificados correctamente en el conjunto de prueba.
 * Gráfica de la Frontera de Decisión: Una visualización en 2D que muestra cómo el clasificador divide el espacio mediante un kernel (como el kernel RBF o Gaussiano).
5. Recursos
 * Entorno de desarrollo: Python en Google Colab o Jupyter Notebook.
 * Librerías principales:
   * scikit-learn (para generar los datos con make_moons, entrenar el SVC con kernel RBF y dividir los datos en entrenamiento/prueba).
   * Matplotlib y NumPy (para graficar los puntos y visualizar de forma gráfica la separación de las lunas).
 * Hardware: Computadora personal estándar con recursos mínimos (al ser datos sintéticos, el entrenamiento toma una fracción de segundo).
6. Riesgos
 * Sobreajuste (Overfitting): Si se configuran mal los hiperparámetros del kernel RBF (como el parámetro de regularización C o gamma), el modelo podría intentar rodear cada punto con demasiada precisión, fallando ante datos nuevos.
 * Subajuste (Underfitting): Si se utiliza un kernel lineal por error, el modelo no podrá separar las lunas porque la separación es curva, lo que daría una pésima exactitud.

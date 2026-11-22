# Propuesta (Hito 1) – Clasificación de patrones no lineales con SVM (make_moons)

**Equipo 5** 
· A: Juan Pablo Miranda Ramirez 25690164
· B: Ricardo Pinete Martinez    25690191
· C: Karla Teodora Galván Acuña 25690704

## 1. Problema y usuarios
Muchos problemas reales (diagnóstico, detección de fraude, control de calidad) tienen
clases que **no se separan con una línea recta**. El proyecto muestra cómo un SVM con
kernel RBF aprende esa frontera curva y la sirve como API. Usuarios: estudiantes y
docentes de aprendizaje automático que quieren explorar, con un clic, cómo clasifica el
modelo cada punto del plano y compararlo con un modelo lineal.

## 2. Datos
- Fuente: `sklearn.datasets.make_moons` (datos **sintéticos** generados en `entrenar.py`;
  no hay descarga). Documentación: https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_moons.html
- Licencia: scikit-learn es BSD-3-Clause; los datos se generan, no hay restricciones.
- Registros: 1 000 puntos (700 entrenamiento, 300 prueba), `random_state=42`, `noise=0.25`.
- Entradas: `x1`, `x2` (coordenadas en el plano). Salida: clase 0 (luna superior) o 1 (luna inferior).
- Generados por: el propio equipo (reproducible con la semilla).

## 3. Algoritmo y por qué es adecuado
**Clasificación** con SVM (`SVC`, kernel RBF, C=1, gamma="scale") precedido de
`StandardScaler`. El kernel RBF proyecta implícitamente los puntos a un espacio donde las
lunas sí son separables. Como referencia se entrena un SVM lineal, que no puede separarlas.

## 4. Métrica objetivo
**Exactitud ≥ 0.90 y F1 macro ≥ 0.90** sobre el 30 % de prueba (y el SVM RBF debe superar
al SVM lineal). El CI falla si la exactitud baja de 0.90.

## 5. Recursos de cómputo
Medidos con `python modelo/entrenar.py` (imprime tiempo y memoria pico de Python):
- Tiempo de entrenamiento: 0.07s 
- Memoria pico: 0.3 MB
- Para servir: 1 vCPU y 512 MB (plan gratuito de Render) bastan; el modelo pesa pocos KB.

## 6. Riesgos iniciales
1. **Datos sintéticos**: no representan ruido ni sesgos reales; la conclusión no se generaliza sin validar con datos reales.
2. **Ruido y traslape** entre lunas: con ruido alto la métrica baja (el umbral 0.90 podría no cumplirse); se controla con la semilla y se documenta.
3. **Costo/latencia**: `probability=True` encarece el entrenamiento y el plan gratuito de Render "duerme" el servicio (arranque en frío de decenas de segundos).

## 7. Reparto
| Hito | A | B | C |
|---|---|---|---|
| 1 Propuesta | repositorio y propuesta | datos y métrica | riesgos y recursos |
| 2 Modelo/API/contenedor | `entrenar.py` y pruebas | `main.py` e `index.html` | Dockerfile y CI |
| 3 Despliegue | Render (`render.yaml`) | mediciones (carga o HPA) | perímetro y reporte |

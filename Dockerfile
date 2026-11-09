# Imagen de ClasificaIA: API + modelo entrenado dentro de la imagen.
FROM python:3.12-slim
WORKDIR /srv
# Primero las dependencias: si solo cambia el código, Docker reutiliza esta capa.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ ./app/
COPY modelo/ ./modelo/
# Entrenar al construir garantiza la misma versión de scikit-learn al entrenar y servir
RUN python modelo/entrenar.py
# Usuario sin privilegios: si alguien vulnera la API, no es root en el contenedor
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
# La salud (/health) la revisan Kubernetes (probes) y Render (healthCheckPath).
# Render indica el puerto en la variable PORT; en local se usa 8000
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
"""API de clasificación de patrones no lineales (SVM + make_moons) con FastAPI.

Endpoints:
  GET  /         página web (app/index.html)
  GET  /health   estado del servicio, versión y métricas del modelo
  GET  /muestra  200 puntos de prueba para dibujar la gráfica
  POST /predict  recibe (x1, x2) y devuelve la luna y la confianza
  GET  /docs     documentación automática de FastAPI
"""
import hmac
import os
from pathlib import Path

import joblib
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

# ---------------------------------------------------------------- Modelo
CARPETA = Path(__file__).parent
# Se carga UNA sola vez al iniciar el servidor.
ARTEFACTO = joblib.load(os.getenv("MODELO_PATH", CARPETA / "modelo.joblib"))

# ---------------------------------------------------------------- Seguridad (Hito 4)
MOSTRAR_DOCS = os.getenv("MOSTRAR_DOCS", "1") == "1"   # 0 oculta /docs
API_KEY = os.getenv("API_KEY", "")                     # vacía = API abierta

app = FastAPI(title="SVM make_moons", version=ARTEFACTO["version"],
              docs_url="/docs" if MOSTRAR_DOCS else None,
              redoc_url=None,
              openapi_url="/openapi.json" if MOSTRAR_DOCS else None)


def requiere_llave(x_api_key: str = Header(default="")):
    """401 si falta la llave y 403 si es incorrecta (solo si API_KEY está definida)."""
    if not API_KEY:
        return
    if not x_api_key:
        raise HTTPException(401, "Falta la cabecera x-api-key")
    if not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(403, "Llave inválida")


# ---------------------------------------------------------------- Entrada
class Punto(BaseModel):
    """Un punto del plano. make_moons produce x1 en [-1.5, 2.5] y x2 en [-1, 1.5]
    aprox.; los límites dejan margen y rechazan valores absurdos con 422."""
    x1: float = Field(ge=-3, le=4)
    x2: float = Field(ge=-3, le=3)


# ---------------------------------------------------------------- Endpoints
@app.get("/health")
def salud():
    """Lo consultan Docker, Kubernetes y Render para saber si el servicio está vivo."""
    return {"status": "ok", "version": ARTEFACTO["version"],
            "exactitud": ARTEFACTO["exactitud"], "f1": ARTEFACTO["f1"]}


@app.get("/muestra")
def muestra():
    """Puntos de prueba [x1, x2, clase] para la gráfica de la página."""
    return {"clases": ARTEFACTO["clases"], "puntos": ARTEFACTO["muestra"]}


@app.post("/predict", dependencies=[Depends(requiere_llave)])
def predecir(p: Punto):
    """Devuelve la luna más probable y su probabilidad (200), o 422 si es inválido."""
    x = [[p.x1, p.x2]]  # una fila, columnas en el MISMO orden que al entrenar
    probabilidades = ARTEFACTO["modelo"].predict_proba(x)[0]
    i = int(probabilidades.argmax())
    return {"clase": ARTEFACTO["clases"][i], "clase_id": i,
            "confianza": round(float(probabilidades[i]), 3)}


@app.get("/", response_class=HTMLResponse)
def inicio():
    """Sirve la página; página y API comparten origen, así que no hay CORS."""
    return (CARPETA / "index.html").read_text(encoding="utf-8")

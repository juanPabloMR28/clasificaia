from pydantic import BaseModel, Field
from typing import List

class DigitsInput(BaseModel):
    pixels: List[float] = Field(..., min_items=64, max_items=64, description="Lista de 64 valores de píxeles (0 a 16)")

<<<<<<< HEAD
@app.post("/predict")
def predecir(data: DigitsInput):
    features = [data.pixels]
    prediccion = int(modelo.predict(features)[0])
    confianza = float(modelo.predict_proba(features)[0].max())
    
    return {
        "clase_predicha": NOMBRES_CLASES[prediccion],
        "confianza": confianza
    }
=======
# ---------------------------------------------------------------- Seguridad (Hito 4)
# MOSTRAR_DOCS=0 en producción oculta /docs (menos información para un atacante).
MOSTRAR_DOCS = os.getenv("MOSTRAR_DOCS", "1") == "1"
# API_KEY: si se define (variable de entorno en Render, nunca en el código), /predict
# exige la cabecera x-api-key con ese valor. Vacía = API abierta (Hitos 1 a 3).
API_KEY = os.getenv("API_KEY", "")

app = FastAPI(title="ClasificaIA", version=ARTEFACTO["version"],
              docs_url="/docs" if MOSTRAR_DOCS else None,
              redoc_url=None, openapi_url="/openapi.json" if MOSTRAR_DOCS else None)

def requiere_llave(x_api_key: str = Header(default="")):
    """Dependencia de FastAPI: 401 si falta la llave y 403 si es incorrecta."""
    if not API_KEY:
        return # sin llave configurada: acceso libre
    if not x_api_key:
        raise HTTPException(401, "Falta la cabecera x-api-key")
    if not hmac.compare_digest(x_api_key, API_KEY): # comparación en tiempo constante
        raise HTTPException(403, "Llave inválida")

# ---------------------------------------------------------------- Entrada
from pydantic import BaseModel, Field

class MoonsInput(BaseModel):
    x1: float = Field(..., ge=-3.0, le=3.0, description="Coordenada X1 en el plano")
    x2: float = Field(..., ge=-3.0, le=3.0, description="Coordenada X2 en el plano")

# ---------------------------------------------------------------- Endpoints
@app.get("/health")
def salud():
    """Lo consultan Docker, Kubernetes y Render para saber si el servicio está vivo."""
    return {"status": "ok", "version": ARTEFACTO["version"],
            "exactitud": ARTEFACTO["exactitud"]}

@app.post("/predict", dependencies=[Depends(requiere_llave)])
def predecir(f: Flor):
    """Devuelve la clase más probable y su probabilidad (200), o 422 si los datos no
    son válidos."""
    # El modelo espera una lista de filas; aquí hay una sola fila con 4 columnas
    # en el MISMO orden que en el entrenamiento.
    x = [[f.largo_sepalo, f.ancho_sepalo, f.largo_petalo, f.ancho_petalo]]
    probabilidades = ARTEFACTO["modelo"].predict_proba(x)[0]
    i = int(probabilidades.argmax()) # índice de la clase ganadora
    return {"clase": ARTEFACTO["clases"][i],
            "confianza": round(float(probabilidades[i]), 3)}

@app.get("/", response_class=HTMLResponse)
def inicio():
    """Sirve la página web; esta y la API comparten origen, así que no hay CORS."""
    return (CARPETA / "index.html").read_text(encoding="utf-8")
>>>>>>> 0797e2d (Ajustes del proyecto)

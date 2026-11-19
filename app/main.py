from pydantic import BaseModel, Field
from typing import List

class DigitsInput(BaseModel):
    pixels: List[float] = Field(..., min_items=64, max_items=64, description="Lista de 64 valores de píxeles (0 a 16)")

@app.post("/predict")
def predecir(data: DigitsInput):
    features = [data.pixels]
    prediccion = int(modelo.predict(features)[0])
    confianza = float(modelo.predict_proba(features)[0].max())
    
    return {
        "clase_predicha": NOMBRES_CLASES[prediccion],
        "confianza": confianza
    }

"""Pruebas automáticas de la API (se ejecutan con: pytest -q).

TestClient simula peticiones HTTP sin levantar un servidor. GitHub Actions las
ejecuta en cada push: si una falla, la imagen no se publica.
"""
from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_health():
    """El servicio responde y reporta la versión del modelo."""
    assert cliente.get("/health").json()["status"] == "ok"


def test_predict_setosa():
    """Una flor típica de la especie setosa se clasifica bien."""
    r = cliente.post("/predict", json={"largo_sepalo": 5.1, "ancho_sepalo": 3.5,
                                       "largo_petalo": 1.4, "ancho_petalo": 0.2})
    assert r.status_code == 200 and r.json()["clase"] == "setosa"


def test_predict_invalido():
    """Un valor negativo se rechaza con 422 (validación de Pydantic)."""
    r = cliente.post("/predict", json={"largo_sepalo": -1, "ancho_sepalo": 3.5,
                                       "largo_petalo": 1.4, "ancho_petalo": 0.2})
    assert r.status_code == 422


def test_calidad_minima():
    """Prueba de calidad: si el modelo baja de 0.85 de exactitud, el CI falla.
    
    >>> En su proyecto: ajusten la métrica y el umbral a su problema.
    """
    assert cliente.get("/health").json()["exactitud"] >= 0.85
def test_llave_requerida(monkeypatch):
    """Hito 4: con API_KEY definida, sin cabecera da 401 y con la correcta da 200."""
    import app.main as m
    monkeypatch.setattr(m, "API_KEY", "secreto-de-prueba")
    flor = {"largo_sepalo": 5.1, "ancho_sepalo": 3.5,
            "largo_petalo": 1.4, "ancho_petalo": 0.2}
    assert cliente.post("/predict", json=flor).status_code == 401
    r = cliente.post("/predict", json=flor, headers={"x-api-key": "secreto-de-prueba"})
    assert r.status_code == 200
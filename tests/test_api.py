"""Pruebas automáticas de la API (pytest -q). Si una falla, la imagen no se publica."""
from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_health():
    """El servicio responde y reporta versión y métricas del modelo."""
    j = cliente.get("/health").json()
    assert j["status"] == "ok" and "f1" in j


def test_predict_luna_superior():
    """Un punto sobre el centro de la luna superior se clasifica como clase 0."""
    r = cliente.post("/predict", json={"x1": 0.0, "x2": 1.0})
    assert r.status_code == 200 and r.json()["clase"] == "luna_superior"


def test_predict_luna_inferior():
    """Un punto sobre el centro de la luna inferior se clasifica como clase 1."""
    r = cliente.post("/predict", json={"x1": 1.0, "x2": -0.5})
    assert r.status_code == 200 and r.json()["clase"] == "luna_inferior"


def test_predict_invalido():
    """Valores fuera de rango o faltantes se rechazan con 422 (Pydantic)."""
    assert cliente.post("/predict", json={"x1": 100, "x2": 0}).status_code == 422
    assert cliente.post("/predict", json={"x1": 0}).status_code == 422


def test_muestra():
    """La muestra para la gráfica trae puntos [x1, x2, clase]."""
    j = cliente.get("/muestra").json()
    assert len(j["puntos"]) == 200 and len(j["puntos"][0]) == 3


def test_calidad_minima():
    """Prueba de calidad: si la exactitud baja de 0.90 (métrica objetivo), el CI falla."""
    assert cliente.get("/health").json()["exactitud"] >= 0.90


def test_llave_requerida(monkeypatch):
    """Hito 4: con API_KEY definida, sin cabecera da 401 y con la correcta da 200."""
    import app.main as m
    monkeypatch.setattr(m, "API_KEY", "secreto-de-prueba")
    punto = {"x1": 0.0, "x2": 1.0}
    assert cliente.post("/predict", json=punto).status_code == 401
    r = cliente.post("/predict", json=punto, headers={"x-api-key": "secreto-de-prueba"})
    assert r.status_code == 200

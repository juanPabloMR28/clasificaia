# Proyecto equipo5 – SVM con make_moons

Clasificación de patrones no lineales: SVM (kernel RBF) sobre datos sintéticos `make_moons`,
servido con FastAPI, empaquetado en Docker, con CI en GitHub Actions y despliegue en Render.

## Ejecutar en VS Code (terminal integrada, desde la raíz)
```bash
python -m venv .venv
source .venv/bin/activate        # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python modelo/entrenar.py        # genera app/modelo.joblib e imprime métricas
pytest -q                        # 7 passed
uvicorn app.main:app --reload    # http://localhost:8000  y  /docs
```
## Contenedor
```bash
docker build -t proyecto:1.0 . && docker run -p 8000:8000 proyecto:1.0
```
## Kubernetes (Opción B del Hito 3)
```bash
docker build -t svm-moons:1.0 . && kind load docker-image svm-moons:1.0 --name proyecto
kubectl apply -f k8s/app.yaml && kubectl get hpa -w
```
## Carga (Opción A del Hito 3)
```bash
python scripts/carga.py https://proyecto-equipo5.onrender.com 200 20
```
## Etiquetas de entrega
`git tag hito1 && git push --tags` (igual para hito2 y hito3).

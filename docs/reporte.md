# Reporte del proyecto (Parte I) – SVM con make_moons

## Hito 1 – Propuesta
Ver `docs/propuesta.md`. Etiqueta: `hito1`.

## Hito 2 – Modelo, API y contenedor
- Resultado de `python modelo/entrenar.py` (pegar): exactitud=____ f1=____ SVM lineal=____
- Captura de `pytest -q` (7 passed): ____
- Captura de `/docs` y de la página: ____
- CI en **rojo** (rompimos el modelo con, por ejemplo, `SVC(kernel="linear")` o `C=0.0001`): captura ____
- CI en **verde** tras corregir + imagen en Packages (GHCR, pública): captura ____
Etiqueta: `hito2`.

## Hito 3 – Despliegue
- URL pública: https://proyecto-equipo5.onrender.com
- `render.yaml` en el repositorio; un `git push` redespliega (captura de Events).

### Mediciones (Opción A: carga y arranque en frío en Render)
`python scripts/carga.py https://proyecto-equipo5.onrender.com 200 20`

| Peticiones | Simultáneas | Éxito | Peticiones/s | p50 (ms) | p95 (ms) |
|---|---|---|---|---|---|
| 50 | 20 | | | | |
| 200 | 20 | | | | |
| 500 | 20 | | | | |
| 1.ª petición tras 20 min sin uso (arranque en frío) | 1 | | | | |

Análisis (con sus palabras): ____

### Perímetro mínimo
Verificación: `curl -I http://proyecto-equipo5.onrender.com` (debe redirigir a https);
la API no responde en otros puertos; `/docs` sigue visible (se oculta en el Hito 4).

| Puerto | Origen | Motivo |
|---|---|---|
| 443/TCP | 0.0.0.0/0 (Internet) | HTTPS: página y API; Render termina TLS |
| 80/TCP | 0.0.0.0/0 (Internet) | Solo redirige a HTTPS |
| 8000/TCP | solo red interna del contenedor | Puerto de uvicorn; no expuesto a Internet |
| 22/TCP y demás | ninguno (cerrado) | No hay acceso remoto ni otros servicios |

En un proveedor con grupos de seguridad (p. ej. AWS): un grupo de seguridad para el
balanceador que permita 443 y 80 desde 0.0.0.0/0, y otro para la instancia/contenedor que
permita 8000 **solo desde el grupo del balanceador**; todo lo demás denegado por defecto.
Etiqueta: `hito3`.

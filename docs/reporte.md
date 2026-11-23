# Reporte del proyecto (Parte I) – SVM con make_moons

## Hito 1 – Propuesta
Ver `docs/propuesta.md`. Etiqueta: `hito1`.

## Hito 2 – Modelo, API y contenedor
- exactitud=0.963 f1=0.963 SVM lineal=0.887

## Hito 3 – Despliegue
- URL pública: https://proyecto-equipo5.onrender.com
- `render.yaml` en el repositorio; un `git push` redespliega (captura de Events).

### Perímetro mínimo
Verificación: `curl -I https://proyecto-equipo5.onrender.com` (debe redirigir a https);
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

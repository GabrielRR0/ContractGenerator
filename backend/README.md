# Backend — Contract Generator (FastAPI)

API que genera contratos en PDF a partir de un formulario. Todo el procesamiento ocurre dentro de la misma request HTTP (sin colas, sin workers en segundo plano), para que funcione en un hosting serverless gratuito sin cold-starts largos.

## 1. Que hace este backend, en una linea

Recibe `{template_id, style_id, data}` por `POST /api/contracts/generate` y devuelve el PDF armado, combinando el **contenido** (definido por la plantilla) con el **diseño visual** (definido por el estilo).

## 2. Requisitos

- Python 3.12+ instalado (`python --version` para verificar).
- No hace falta Postgres, Docker, ni ningun servicio externo — el backend corre 100% local con solo Python.

## 3. Como ejecutarlo paso a paso

Todos los comandos se corren **desde la carpeta `backend/`**.

### 3.1 Crear el entorno virtual (solo la primera vez)

```
python -m venv .venv
```

Esto crea la carpeta `.venv/` con una copia aislada de Python + sus librerias, para no mezclar las dependencias de este proyecto con las de tu sistema o con las de otros proyectos.

### 3.2 Activar el entorno virtual (cada vez que abras una terminal nueva)

El comando depende de la terminal que uses — **este es el paso donde mas suele fallar** si se usa el comando equivocado (el sintoma tipico: `pytest` corre pero tira `ModuleNotFoundError: No module named 'app'` o `'fastapi'`, porque en realidad esta usando el Python global de Windows, no el de `.venv`).

**PowerShell** (la terminal por defecto en Windows/VS Code, el prompt empieza con `PS `):
```powershell
.venv\Scripts\Activate.ps1
```
Si da un error de "la ejecucion de scripts esta deshabilitada en este sistema", correr una vez por sesion de terminal:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
y volver a intentar `.venv\Scripts\Activate.ps1`.

**cmd.exe** (Simbolo del sistema):
```
.venv\Scripts\activate.bat
```

**Git Bash / bash**:
```
source .venv/Scripts/activate
```

En cualquiera de los tres casos vas a ver `(.venv)` al inicio de la linea de la terminal — confirma que `python`/`pip`/`pytest`/`uvicorn` ahora apuntan al entorno del proyecto, no al Python global.

**Alternativa a prueba de fallos** (si activar el venv da problemas): invocar siempre el ejecutable de `.venv` de forma explicita, sin activar nada:
```
.venv\Scripts\python.exe -m pytest
.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

### 3.3 Instalar las dependencias (solo la primera vez, o si `requirements.txt` cambio)

```
pip install -r requirements.txt
```

Lee `requirements.txt` (la lista congelada de librerias y sus versiones exactas) y las instala dentro de `.venv/`.

### 3.4 Levantar el servidor

```
uvicorn app.main:app --reload --port 8000
```

- **`uvicorn`**: el servidor ASGI que ejecuta la aplicacion FastAPI (FastAPI define la app, uvicorn la sirve por HTTP).
- **`app.main:app`**: le dice a uvicorn donde esta la aplicacion — "en el archivo `app/main.py`, la variable llamada `app`" (la instancia de `FastAPI()`).
- **`--reload`**: reinicia el servidor automaticamente cada vez que guardas un cambio en el codigo. Util en desarrollo, no se usa en produccion.
- **`--port 8000`**: puerto en el que escucha. El frontend (Vite) ya esta configurado para redirigir `/api` hacia `http://localhost:8000`, asi que si cambias el puerto aca tambien hay que actualizar `frontend/vite.config.ts`.

Para detenerlo: `Ctrl+C` en la misma terminal.

### 3.5 Probarlo sin el frontend

Con el servidor corriendo, abri en el navegador:

```
http://localhost:8000/docs
```

FastAPI genera automaticamente esta UI interactiva (Swagger UI) a partir de los schemas de Pydantic — permite probar cada endpoint (`GET /api/contracts/templates`, `GET /api/contracts/styles`, `POST /api/contracts/generate`) sin escribir codigo ni usar Postman.

## 4. Como correr los tests

```
pytest
```

**Importante**: esto solo encuentra `fastapi` y `app` si el venv esta activo (ver 3.2) — si ves `ModuleNotFoundError`, es señal de que `pytest` esta corriendo con el Python global de Windows en vez del de `.venv`. Para descartar el problema de una: `.venv\Scripts\python.exe -m pytest`.

La configuracion en `pytest.ini` (`-v -s`) hace que se vea, para cada test: que esta probando (`print` antes de la aserción) y el resultado (`PASSED`/`FAILED`). Los tests que generan un PDF real lo guardan en disco para poder abrirlo:

- `tests/services/contracts/output/nda_minimal.pdf`
- `tests/routers/contracts/output/nda_minimal_via_api.pdf`

Esas carpetas `output/` son artefactos de test (no se versionan, ver `.gitignore`).

## 5. Estructura del proyecto

```
app/
  main.py                       # entrypoint: crea la app FastAPI, monta CORS y el router
  config.py                     # configuracion via variables de entorno (.env)
  routers/contracts/            # capa HTTP (endpoints) -> ver README.md de la carpeta
  services/contracts/           # logica de negocio (orquestacion, plantillas, PDF) -> ver README.md de la carpeta
  schemas/contracts/            # validacion de datos (Pydantic) -> ver README.md de la carpeta
  shared/storage/               # cliente de Supabase (sin implementar todavia, ver mas abajo) -> ver README.md de la carpeta
tests/                          # espejo de app/, un archivo de test por modulo con logica
pytest.ini                      # configuracion de pytest (verbose + prints visibles)
requirements.txt                # dependencias congeladas (pip freeze)
.env.example                    # variables de entorno esperadas (copiar a .env si se usan)
```

No hay ningun `__init__.py` en estas carpetas — Python (desde la version 3.3) reconoce una carpeta como paquete importable solo por su estructura, sin necesitar ese archivo (namespace packages implicitos). Cada carpeta con logica real tiene su propio `README.md` explicando que hace cada archivo puntual.

## 6. De donde sale cada PDF (flujo interno)

1. El frontend hace `POST /api/contracts/generate` con `{template_id: "nda", style_id: "minimal", data: {...}}`.
2. `routers/contracts/contracts_router.py` valida el body contra `GenerateContractRequest` (Pydantic) y llama a `contract_service.generate_document(request)`.
3. `services/contracts/contract_service.py` busca la plantilla (`nda_template.py`) y le pide que arme el **contenido** (titulo, parrafos, firmas) a partir de los datos del formulario.
4. Ese contenido se pasa a `services/contracts/pdf/generator.py`, que busca el **estilo** elegido (`style_minimal.py`) y le delega el dibujo del PDF completo con `fpdf2`.
5. El router devuelve los bytes del PDF directamente en la respuesta HTTP (`Content-Type: application/pdf`), no como JSON — asi el navegador lo descarga sin pasos intermedios.

## 7. Sobre Supabase (historial de documentos)

`shared/storage/` existe como carpeta preparada pero **no tiene ningun cliente implementado todavia**. La razon: para lo que seria guardar (unos pocos campos de texto por documento generado), levantar una base de datos Postgres completa via Supabase es sobredimensionado — no hay volumen ni consultas complejas que lo justifiquen hoy. Se implementa recien si aparece un requisito real (ej. mostrar un historial de documentos generados en la UI), no antes.

## 8. Variables de entorno y despliegue

Copiar `.env.example` a `.env` y completar segun corresponda:

- `SUPABASE_URL` / `SUPABASE_KEY`: sin uso todavia (ver seccion 7).
- `FRONTEND_URL`: la URL del frontend en produccion (ej. `https://contract-generator-tuusuario.vercel.app`). Se suma a la lista de origenes permitidos por CORS en `app/main.py`, junto a `http://localhost:5173` (que **siempre** queda permitido, para que `npm run dev` funcione sin configurar nada). Sin esta variable, cualquier request desde un dominio que no sea `localhost:5173` es rechazada por el navegador (error de CORS), aunque el backend este funcionando bien.
- `RATE_LIMIT_GENERATE` / `RATE_LIMIT_PREVIEW` / `RATE_LIMIT_READ`: limites por IP de cada grupo de endpoints (ver seccion 10). Valores por defecto razonables para el uso normal del formulario; no hace falta tocarlos salvo que se quiera ajustar la sensibilidad.
- `RATE_LIMIT_STORAGE_URI`: donde vive el contador del rate limiter. `memory://` (default) alcanza para un solo proceso; en un deploy serverless con varias instancias corriendo en paralelo, cada una cuenta por separado y el limite deja de ser estricto. Para un limite global real, apuntar a Redis (Upstash tiene free tier y combina bien con Vercel).
- `MAX_BODY_BYTES`: tamaño maximo de body aceptado por cualquier endpoint (default 50000 bytes).

Al desplegar (Vercel, Render, Railway, Fly.io, etc.), estas variables se configuran en el panel del servicio, no en un archivo `.env` (ese archivo nunca se sube al repo, ver `.gitignore`).

## 10. Protecciones del backend (rate limiting y hardening)

Como esta API es publica (sin login) y hace trabajo real por request (arma un PDF), tiene protecciones pensadas especificamente contra abuso/DoS barato, no solo validacion de forma:

- **Rate limiting por IP** (`slowapi`, ver `app/core/rate_limit.py`): `/generate` (lo mas costoso) a 10/min, `/preview` a 90/min (se dispara en cada pausa al escribir, no solo al confirmar), `/templates` y `/styles` a 60/min. Al superarlo, responde `429` con headers `X-RateLimit-*`/`Retry-After`. La clave de rate limit es la IP real del cliente leida de `X-Forwarded-For` — necesario porque en Vercel (y cualquier PaaS detras de un edge/proxy) `request.client.host` es la IP del proxy, no la del usuario, y sin esto el limite terminaria compartido por todo el trafico.
- **Limite de tamaño de body** (middleware en `app/main.py`): cualquier request con `Content-Length` mayor a `MAX_BODY_BYTES` se corta con `413` antes de llegar a Pydantic o a `fpdf2`. Se basa en el header, no en contar bytes en streaming, asi que no cubre un body chunked sin `Content-Length` declarado — cubre el caso normal (fetch/axios/curl siempre lo declaran).
- **`max_length` en los campos de texto** de cada plantilla (`services/contracts/templates/*.py`): defensa en profundidad ademas del limite de body — evita que un solo campo (ej. una clausula) sea desproporcionadamente largo y encarezca el renderizado del PDF, con un error 422 preciso en vez de un 413 generico. Solo aplica a `/generate` (que valida contra un modelo Pydantic fijo por plantilla); `/preview` es intencionalmente tolerante a datos incompletos y queda cubierto igual por el limite de body.
- **Headers de seguridad** (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`) en todas las respuestas.
- **CORS ya restringido** a `localhost:5173` + `FRONTEND_URL` (ver seccion 8) — importante: CORS es una regla que respetan los navegadores, no una barrera real contra un cliente que le pega directo a la API (curl, Postman, otro backend). Para esta app (sin datos sensibles ni autenticacion) alcanza; si en el futuro maneja datos reales de usuarios, ahi si conviene sumar autenticacion.

## 9. Decisiones de arquitectura (por que esta asi)

- **fpdf2 en vez de WeasyPrint**: WeasyPrint depende de librerias nativas de sistema (Pango/Cairo) que no siempre estan disponibles en runtimes serverless y aumentan el cold-start. fpdf2 es pure-Python.
- **El PDF se genera siempre en la misma request** (nunca en background/cola): cumple la regla del proyecto de "cero colas persistentes, cero workers 24/7".
- **El preview de estilo se resuelve en el frontend**, no pegandole al backend en cada cambio de estilo elegido (ver `frontend/README.md`).
- **Sin `__init__.py`**: se eligio namespace packages implicitos por preferencia del equipo; funcionalmente es identico a tener los archivos, solo cambia que la documentacion de cada paquete vive en el `README.md` de la carpeta en vez de en el `__init__.py`.
- **`pythonpath = .` en `pytest.ini`**: al no haber `__init__.py`, pytest no siempre agrega automaticamente `backend/` al path de Python al correr `pytest` directo (si o solo `python -m pytest`) — sin esta linea, los tests fallan con `ModuleNotFoundError: No module named 'app'` aunque el venv este bien activado. Esta linea lo hace explicito y funciona igual para ambas formas de invocar los tests.
- **`FRONTEND_URL` como variable de entorno, no hardcodeada**: el dominio de produccion del frontend no se conoce hasta desplegarlo, y puede cambiar (ej. si se recrea el proyecto en el hosting). Leerlo de `.env`/config del servicio evita tener que tocar codigo y volver a desplegar solo para actualizar un dominio.
- **`CORSMiddleware` se agrega al final en `app/main.py`**: Starlette envuelve los middlewares en orden inverso al que se agregan (el ultimo agregado queda "mas afuera"). Si CORS quedara mas adentro que el middleware de limite de body o el rate limiter, una respuesta cortada temprano (413/429) nunca pasaria por CORS y el navegador la mostraria como error de CORS en vez del error real, rompiendo el manejo de errores del frontend.

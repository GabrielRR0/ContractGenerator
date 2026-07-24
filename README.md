# Contract Generator

## Problema que resuelve

Empresas que redactan contratos, cotizaciones o NDAs a mano en Word, perdiendo tiempo y consistencia visual. Este servicio genera el PDF a partir de un formulario y una plantilla, con estilo visual elegido por el usuario.

## Estado actual

Camino feliz completo: plantilla **NDA** + estilo **minimalista**, end-to-end (formulario → PDF descargado). Las demás combinaciones (cotización, contrato de servicio, estilos corporativo y clásico) y el historial vía Supabase quedan como siguiente iteración, reutilizando `generator.py` y el mismo patrón de `templates/`/`styles/`.

## Stack

- Backend: FastAPI + [fpdf2](https://github.com/py-pdf/fpdf2) (generación de PDF pure-Python, sin dependencias de sistema — evita cold-starts largos en serverless).
- Frontend: Vue 3 (Composition API + `<script setup>`) + Vite + TypeScript.

## Diseño visual

El estilo de todas las pantallas de este proyecto (y del resto del portafolio) sigue [`../DESIGN.md`](../DESIGN.md) — guía de principios, color, tipografía, espaciado y animaciones (estilo moderno, minimalista, tipo Apple). Cualquier componente Vue nuevo debe respetar esa guía antes de escribir CSS propio.

## Cómo probarlo

**Backend:**
```
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Frontend** (en otra terminal):
```
cd frontend
npm install
npm run dev
```

Abrir la URL que imprime Vite (por defecto `http://localhost:5173`), completar el formulario del NDA y hacer clic en "Generar PDF".

## Cómo correr los tests

- Backend: `cd backend && pytest`
- Frontend: `cd frontend && npm run test`

## Decisiones de arquitectura

- **fpdf2 en vez de WeasyPrint**: WeasyPrint depende de librerías nativas de sistema (Pango/Cairo) que no siempre están disponibles en runtimes serverless y aumentan el cold-start. fpdf2 es pure-Python.
- **Preview de estilo resuelto en el frontend**: para evitar llamadas al backend en cada cambio de estilo, el preview es una maqueta HTML/CSS basada en la metadata de `/api/contracts/styles`. El PDF real solo se genera una vez, al confirmar el formulario.
- **`POST /api/contracts/generate` devuelve el PDF binario directo** (no JSON con base64), para que el navegador lo descargue sin pasos intermedios.
- **Sin librería de formularios multi-paso ni Supabase todavía**: con un solo paso de formulario no se justifica una dependencia extra; Supabase (historial) se agrega recién cuando el camino feliz esté validado.
- **Vitest con `pool: 'threads'`**: el pool por defecto (`forks`) no arranca en este entorno de desarrollo; con `threads` corre sin problema.

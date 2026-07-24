# shared/storage

Cliente de acceso a Supabase (Postgres + Storage), compartido por cualquier dominio que necesite persistencia (hoy ninguno lo usa todavia).

## Estado actual

Vacio (solo el `__init__.py`). Se implementa `supabase_client.py` recien cuando se agregue el historial de documentos generados (funcionalidad opcional del proyecto, deferida hasta validar el camino feliz de generacion de PDF). Cuando se cree, expondra un cliente configurado con `SUPABASE_URL`/`SUPABASE_KEY` (ver `app/config.py`) para que `contract_service.py` lo use al guardar/consultar el historial.

## Por que esta carpeta esta en `shared/` y no en `services/contracts/`

El cliente de Supabase no es especifico del dominio "contratos" — los demas proyectos del portafolio (compartidor de archivos, digitalizador de facturas, etc.) tambien lo usaran. Vive en `shared/` para no atarlo a un dominio particular.

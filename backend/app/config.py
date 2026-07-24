from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    supabase_url: str = ""
    supabase_key: str = ""
    # URL del frontend desplegado (produccion), para habilitarla en CORS sin
    # hardcodear el dominio en el codigo. En dev, localhost:5173 siempre
    # queda permitido ademas de esta (ver app/main.py).
    frontend_url: str = ""

    # Backend de almacenamiento del rate limiter (slowapi/limits). "memory://"
    # alcanza para un solo proceso; en serverless con multiples instancias
    # (p.ej. Vercel con trafico alto) el limite deja de ser estricto porque
    # cada instancia cuenta por separado. Para un limite global real, apuntar
    # a Redis (Upstash tiene free tier): "redis://default:<pass>@<host>:<port>".
    rate_limit_storage_uri: str = "memory://"
    # Limite del endpoint mas costoso (genera el PDF).
    rate_limit_generate: str = "10/minute"
    # Preview se llama mientras el usuario escribe, pero sigue siendo trabajo
    # de CPU por request; limite mas laxo que generate.
    rate_limit_preview: str = "30/minute"
    # Catalogos de solo lectura (templates/styles): limite laxo, mas que nada
    # anti-scraping/abuso automatizado.
    rate_limit_read: str = "60/minute"

    # Tamano maximo de body aceptado (bytes). Los payloads reales de este
    # formulario pesan pocos KB; este limite es una defensa barata contra
    # requests gigantes antes de que lleguen a Pydantic/fpdf2.
    max_body_bytes: int = 20_000


settings = Settings()

from fastapi import APIRouter, HTTPException, Request, Response

from app.config import settings
from app.core.rate_limit import limiter
from app.schemas.contracts.contract_schemas import (
    GenerateContractRequest,
    PreviewContractRequest,
    StyleInfo,
    TemplateInfo,
)
from app.services.contracts import contract_service

router = APIRouter(prefix="/api/contracts", tags=["contracts"])


@router.get("/templates", response_model=list[TemplateInfo])
@limiter.limit(settings.rate_limit_read)
def get_templates(request: Request, response: Response, locale: str = "es") -> list[TemplateInfo]:
    # `response: Response` no se usa directamente: FastAPI la inyecta y
    # slowapi le escribe ahi los headers X-RateLimit-*. Sin este parametro,
    # slowapi no tiene donde escribirlos (el valor de retorno es una lista,
    # no un Response) y tira 500 en vez de headers.
    return contract_service.list_templates(locale)


@router.get("/styles", response_model=list[StyleInfo])
@limiter.limit(settings.rate_limit_read)
def get_styles(request: Request, response: Response, locale: str = "es") -> list[StyleInfo]:
    return contract_service.list_styles(locale)


@router.post("/preview")
@limiter.limit(settings.rate_limit_preview)
def preview(request: Request, response: Response, body: PreviewContractRequest) -> dict:
    # Contenido textual (titulo/parrafos/firmas) tolerante a datos
    # incompletos, para el preview en vivo mientras se completa el formulario.
    try:
        return contract_service.preview_document(body.template_id, body.data, body.locale, body.style_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.post("/generate")
@limiter.limit(settings.rate_limit_generate)
def generate(request: Request, body: GenerateContractRequest) -> Response:
    try:
        pdf_bytes = contract_service.generate_document(body)
    except ValueError as exc:
        # template_id/style_id no reconocido o datos incompletos -> error de
        # cliente, no 500.
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    # Se devuelve el binario directo (no JSON/base64) para que el navegador
    # dispare la descarga sin pasos intermedios en el frontend.
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=contrato.pdf"},
    )

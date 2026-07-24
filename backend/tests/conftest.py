import pytest

from app.core.rate_limit import limiter


@pytest.fixture(autouse=True)
def _reset_rate_limiter():
    # El limiter vive en app.state y persiste durante toda la sesion de
    # pytest (el modulo app.main se importa una sola vez); sin resetearlo
    # entre tests, el orden en que corren los archivos de test afectaria si
    # se dispara un 429 o no.
    limiter.reset()
    yield

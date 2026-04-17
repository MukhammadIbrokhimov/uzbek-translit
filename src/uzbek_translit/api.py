"""FastAPI service exposing the transliterator over HTTP."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

from uzbek_translit import __version__, transliterate

Direction = Literal["cyrillic", "latin"]

app = FastAPI(
    title="uzbek-translit",
    description=(
        "Transliterate Uzbek text between Latin and Cyrillic scripts. "
        "Built on a curated lexicon for lossy edge cases (e.g. `ts` vs `с` vs `ц`)."
    ),
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc",
)


class TransliterateRequest(BaseModel):
    """Body for ``POST /transliterate``."""

    text: str = Field(
        ...,
        description="Source text to transliterate.",
        examples=["Assalomu alaykum"],
        min_length=1,
        max_length=50_000,
    )
    direction: Direction = Field(
        ...,
        description="Target script: 'cyrillic' or 'latin'.",
        examples=["cyrillic"],
    )


class TransliterateResponse(BaseModel):
    """Response body for ``POST /transliterate``."""

    result: str = Field(..., description="Transliterated text.")
    direction: Direction = Field(..., description="Target script used.")


class HealthResponse(BaseModel):
    """Response body for ``GET /health``."""

    status: Literal["ok"] = "ok"
    version: str


@app.get("/health", response_model=HealthResponse, tags=["meta"])
def health() -> HealthResponse:
    """Liveness probe. Returns 200 with the service version."""
    return HealthResponse(status="ok", version=__version__)


@app.post(
    "/transliterate",
    response_model=TransliterateResponse,
    tags=["transliterate"],
)
def transliterate_endpoint(req: TransliterateRequest) -> TransliterateResponse:
    """Transliterate Uzbek text to the target script.

    The transliterator handles the full Uzbek alphabet and curated edge
    cases (``ts``, ``е``, ``ё``, ``ю``, ``я``, soft sign, and others) that
    simple character-by-character maps cannot resolve unambiguously.
    """
    result = transliterate(req.text, req.direction)
    return TransliterateResponse(result=result, direction=req.direction)

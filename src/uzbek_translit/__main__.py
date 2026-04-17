"""Run with ``python -m uzbek_translit`` to start the dev server."""

from __future__ import annotations

import uvicorn


def main() -> None:
    """Start the FastAPI service with uvicorn on 0.0.0.0:8000."""
    uvicorn.run(
        "uzbek_translit.api:app",
        host="0.0.0.0",  # noqa: S104 — binding to all interfaces intentional for container
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()

# syntax=docker/dockerfile:1.7

FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies, then the package, then strip caches.
COPY pyproject.toml README.md ./
COPY src/ ./src/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

FROM python:3.12-slim AS runtime

# Run as a non-root user.
RUN useradd --create-home --uid 1001 app
USER app
WORKDIR /home/app

# Copy the site-packages from the builder.
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()" || exit 1

CMD ["uvicorn", "uzbek_translit.api:app", "--host", "0.0.0.0", "--port", "8000"]

# uzbek-translit

[![ci](https://github.com/MukhammadIbrokhimov/uzbek-translit/actions/workflows/ci.yml/badge.svg)](https://github.com/MukhammadIbrokhimov/uzbek-translit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A FastAPI service for transliterating Uzbek text between **Latin** and **Cyrillic** scripts. Modern Uzbek is written in both — this service handles the full alphabet plus curated lexicons for the ambiguous cases that naïve character-by-character maps get wrong.

## Why this is non-trivial

Uzbek transliteration looks like a 1-to-1 character mapping until you hit words where the same Cyrillic grapheme (`ц`, `е`, `ё`, `ю`, `я`, `ь`) corresponds to different Latin digraphs depending on context. Examples:

| Latin | Cyrillic | Why |
|---|---|---|
| **abzats** | абзац | `ts` → `ц`, not `тс`, because of a loanword lexicon |
| **yemak** | емак | word-initial `ye` → `е` |
| **koʻr** | кўр | Latin `oʻ` → Cyrillic `ў` |

This project carries dictionaries of thousands of such exceptions (loanwords, word-beginning rules, after-vowel rules) from the original `uzbek_transliterator` project and exposes them over HTTP.

## API

### `POST /transliterate`

```bash
curl -X POST http://localhost:8000/transliterate \
  -H "Content-Type: application/json" \
  -d '{"text": "Assalomu alaykum", "direction": "cyrillic"}'
# {"result":"Ассалому алайкум","direction":"cyrillic"}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `text` | string | yes | 1–50 000 characters |
| `direction` | `"cyrillic"` \| `"latin"` | yes | target script |

### `GET /health`

```bash
curl http://localhost:8000/health
# {"status":"ok","version":"0.1.0"}
```

### `GET /docs`

Auto-generated Swagger UI. Also available as OpenAPI at `/openapi.json` and ReDoc at `/redoc`.

## Quick start (Docker)

```bash
docker build -t uzbek-translit .
docker run --rm -p 8000:8000 uzbek-translit
# Then open http://localhost:8000/docs
```

## Local development

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run the service (reload on edit):
uvicorn uzbek_translit.api:app --reload

# Or use the console script:
uzbek-translit-serve

# Run tests:
pytest

# Lint + format:
ruff check .
ruff format .
```

## Project layout

```
src/uzbek_translit/
├── __init__.py        # re-exports public API
├── __main__.py        # `python -m uzbek_translit` starts the server
├── api.py             # FastAPI routes and pydantic models
└── transliterate.py   # pure transliteration — no IO, no framework

tests/
├── conftest.py
├── test_transliterate.py  # unit tests on the core library
└── test_api.py            # HTTP tests via FastAPI TestClient

.github/workflows/ci.yml   # ruff + pytest (3.11, 3.12) + docker build
Dockerfile                 # multi-stage, non-root runtime
pyproject.toml             # hatchling build, ruff config, pytest config
```

## Library usage

The transliteration logic is also importable directly:

```python
from uzbek_translit import to_cyrillic, to_latin, transliterate

to_cyrillic("Assalomu alaykum")      # → "Ассалому алайкум"
to_latin("Ассалому алайкум")         # → "Assalomu alaykum"
transliterate("kitob", "cyrillic")   # → "китоб"
```

## Credits

The transliteration tables and rule engine are ported from the standalone [`uzbek_transliterator`](https://github.com/MukhammadIbrokhimov) project (now a private archive). This repo restructures the logic into a packaged library + HTTP service with tests, CI, and a container image.

## License

MIT. See [LICENSE](LICENSE).

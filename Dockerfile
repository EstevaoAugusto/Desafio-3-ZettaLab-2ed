# ──────────────────────────────────────────────────────────────
#  Este Dockerfile deve ficar na RAIZ do projeto, um nível
#  acima de api/. Estrutura esperada:
#
#  projeto/                  ← contexto do build (aqui fica este arquivo)
#  ├── Dockerfile
#  ├── docker-compose.yml
#  ├── pyproject.toml
#  ├── uv.lock
#  ├── api/
#  │   ├── main.py
#  │   ├── config_path_api.py
#  │   ├── routers/
#  │   ├── schemas/
#  │   └── services/
#  ├── scripts/              ← importado por modelos_service.py
#  ├── data/                 ← montado como volume
#  ├── models/               ← montado como volume
#  ├── metrics/              ← montado como volume
#  └── features/             ← montado como volume
# ──────────────────────────────────────────────────────────────


# ── Build stage: instala dependências com uv ──────────────────
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copia lockfiles da raiz do projeto (onde o uv os gerencia)
COPY pyproject.toml uv.lock* ./

# Cria e instala as dependências no venv local
RUN uv venv .venv && uv sync --frozen --no-install-project --no-dev


# ── Runtime stage: imagem final enxuta ────────────────────────
FROM python:3.13-slim AS runtime

WORKDIR /app

# Instalar dependências do sistema para LightGBM (libgomp = OpenMP)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Traz o virtualenv pronto do build stage
COPY --from=builder /app/.venv /app/.venv

# Copia o código da API
COPY api/ ./api/

# Copia scripts/ — necessário pois modelos_service.py faz `import scripts.modeling`
COPY scripts/ ./scripts/

# config_path.py fica na raiz e é importado por scripts/modeling.py
COPY config_path.py ./

# ── Variáveis de ambiente ─────────────────────────────────────
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # /app fica no PYTHONPATH para que `import scripts.modeling`
    # e `import config_path_api` funcionem corretamente
    PYTHONPATH="/app"

# ── Portas ────────────────────────────────────────────────────
EXPOSE 8000

# ── Healthcheck ───────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# ── Comando de inicialização ──────────────────────────────────
# main.py está em api/, mas uvicorn precisa do módulo relativo a /app
# Usar 'python' funciona porque PATH já inclui .venv/bin
CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

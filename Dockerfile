FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# espeak-ng: phonemizer fallback used by kokoro
# build-essential/cmake: needed if pyopenjtalk (Japanese) has no prebuilt wheel for your arch
RUN apt-get update && apt-get install -y --no-install-recommends \
        espeak-ng libsndfile1 build-essential cmake \
    && rm -rf /var/lib/apt/lists/*

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    HF_HOME=/cache/huggingface

WORKDIR /app

# Dependencies first, so this layer is cached until pyproject.toml / uv.lock change.
# uv.lock is optional here: run `uv lock` next to pyproject.toml to pin versions.
COPY pyproject.toml uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-install-project

ENV PATH="/app/.venv/bin:$PATH"

# Japanese dictionary for misaki[ja]
RUN python -m unidic download

COPY tts.py .

ENTRYPOINT ["python", "tts.py"]

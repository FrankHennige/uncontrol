FROM python:3.12-slim

WORKDIR /app

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
RUN pip install uv==0.8.24
ENV PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --group container
# RUN pip install django

COPY example/ .
COPY src/uncontrol ./uncontrol

USER appuser
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
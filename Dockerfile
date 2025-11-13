FROM python:3.12-slim

WORKDIR /app

COPY app /app
COPY mypy.ini /mypy.ini
COPY ruff.toml /ruff.toml
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

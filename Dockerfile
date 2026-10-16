# ── Base Image ────────────────────────────────────────────────────────────────
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# ── Install Dependencies ──────────────────────────────────────────────────────
# Copy requirements first (better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy Project Files ────────────────────────────────────────────────────────
COPY app/ .

# ── Create folder for SQLite database ────────────────────────────────────────
RUN mkdir -p /app/data

ENV PYTHONPATH=/app
ENV PYTHONNUNBUFFERED=1

# ── Expose Ports ──────────────────────────────────────────────────────────────
# FastAPI runs on 8000, Streamlit runs on 8501
EXPOSE 8000
EXPOSE 8501

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

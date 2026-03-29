# Stage 1: Build React frontend
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY frontend/package*.json frontend/
RUN cd frontend && npm install
COPY frontend/ frontend/
RUN cd frontend && npm run build
# vite outputs to ../backend/static → /app/backend/static

# Stage 2: Python runtime
FROM python:3.11-slim
WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
COPY --from=frontend-builder /app/backend/static/ ./static/
EXPOSE 8000
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

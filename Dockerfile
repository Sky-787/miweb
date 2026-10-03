FROM python:3.11-slim
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ /app/
# Render asigna el puerto en la variable de entorno PORT dinámicamente
CMD uvicorn main:app --host 0.0.0.0 --port $PORT

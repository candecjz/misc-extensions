FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Directorio de trabajo
WORKDIR /app

COPY requirements.txt .

# 5. Instalamos dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# 8. Comando de arranque
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


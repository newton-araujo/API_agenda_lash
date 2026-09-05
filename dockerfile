FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

# Ajuste 'app:app' conforme o nome do seu arquivo principal:
# Se o arquivo for 'main.py' e a variável for 'app = Flask(...)', use: main:app
# Se for 'app.py', use: app:app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
# Použijeme oficiální Python image jako základ
FROM python:3.9-slim

# Nastavíme proměnné prostředí pro Python
ENV PYTHONUNBUFFERED True
ENV PYTHONDONTWRITEBYTECODE 1

# Vytvoříme a nastavíme pracovní adresář
WORKDIR /app

# Nejprve zkopírujeme a nainstalujeme requirements
# Toto je optimalizace pro Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pak zkopírujeme zbytek aplikace
COPY . .

# Spustíme Gunicorn s optimální konfigurací pro Cloud Run
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
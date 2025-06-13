# Usa un'immagine ufficiale di Python
FROM python:3.10-slim

# Installa dipendenze di sistema
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libffi-dev libjpeg-dev libpng-dev && \
    apt-get clean

# Crea la directory dell'app
WORKDIR /app

# Copia tutti i file nel container
COPY . /app

# Installa le dipendenze Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Esponi la porta usata da Flask
EXPOSE 8080

# Avvia l'app
CMD ["python", "main.py"]

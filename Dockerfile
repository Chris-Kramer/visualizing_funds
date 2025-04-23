FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
COPY app.py ./
COPY logo.png ./
COPY data/ ./data/
COPY styling/ ./styling/
COPY visualization_modules/ ./visualization_modules/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["streamlit", "run", "app.py", "--server.port=80", "--server.enableCORS=false", "--server.enableXsrfProtection=false"]
# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt ./
COPY app.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit listens on port 8501 by default
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
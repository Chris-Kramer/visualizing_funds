# Use a slim Python 3.11 base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy core files
COPY requirements.txt ./
COPY app.py ./
COPY logo.png ./

# Copy project directories
COPY data/ ./data/
COPY styling/ ./styling/
COPY visualization_modules/ ./visualization_modules/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the default Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
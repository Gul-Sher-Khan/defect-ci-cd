# Dockerfile (simple)
FROM python:3.12-slim

WORKDIR /app

# Install deps (from wheels; no system build tools)
COPY requirements.txt .
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Copy app code and the trained model
COPY src/ ./src/
COPY models/model.pkl ./models/model.pkl

# Env for the app
ENV FLASK_APP=src/app.py
ENV MODEL_PATH=/app/models/model.pkl
ENV LOG_LEVEL=INFO

EXPOSE 5000

# Start the API
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "--chdir", "src", "app:app"]

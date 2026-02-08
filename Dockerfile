FROM python:3.11-slim

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libsndfile1 \
 && rm -rf /var/lib/apt/lists/*

# copy deps first for caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy app
COPY . /app

EXPOSE 8501

ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_RUN_ON_SAVE=false

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true"]

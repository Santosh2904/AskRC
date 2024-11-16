# Use Airflow image with Python 3.11
FROM apache/airflow:2.7.0-python3.11

# Install required system libraries as root
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libstdc++6 \
    python3-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch to the airflow user
USER airflow

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt /requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /requirements.txt

# Install additional resources (e.g., NLTK and SpaCy models)
RUN python -m nltk.downloader vader_lexicon punkt opinion_lexicon
RUN python -m spacy download en_core_web_sm

# Set working directory
WORKDIR /opt/airflow

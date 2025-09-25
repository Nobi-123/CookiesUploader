FROM python:3.10-slim

# Install system deps for Chrome + Selenium
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    chromium chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set envs
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin

# Copy files
WORKDIR /app
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Run bot
CMD ["python", "main.py"]

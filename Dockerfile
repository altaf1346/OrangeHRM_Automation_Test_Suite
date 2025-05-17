FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    libgconf-2-4 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Allure
RUN apt-get update && apt-get install -y openjdk-11-jdk \
    && wget https://github.com/allure-framework/allure2/releases/download/2.24.0/allure-2.24.0.tgz \
    && tar -zxvf allure-2.24.0.tgz -C /opt \
    && ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure \
    && rm allure-2.24.0.tgz \
    && rm -rf /var/lib/apt/lists/*

# Create directories for reports
RUN mkdir -p /app/reports/allure-results /app/reports/screenshots /app/reports/logs

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV BROWSER=chrome
ENV HEADLESS=true

# Run tests with Allure reporting
CMD ["sh", "-c", "pytest --alluredir=reports/allure-results && allure generate reports/allure-results -o reports/allure-report"]
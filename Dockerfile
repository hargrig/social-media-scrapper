# Start from a Python base image
FROM python:3.11-slim

# Update package lists and install dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libcurl3-gnutls \
    libcurl3-nss \
    libcurl4 \
    xdg-utils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV C_FORCE_ROOT=1
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV APP_HOME=/celery_app
ENV APP_USER=scrapper

# Install Chromium
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -O /tmp/chrome.deb \
    && dpkg -i /tmp/chrome.deb \
    && apt-get install -f \
    && rm /tmp/chrome.deb


# Install ChromeDriver
RUN wget -q "https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.83/linux64/chromedriver-linux64.zip" \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm chromedriver-linux64.zip

WORKDIR $APP_HOME

COPY ./requirements.txt .
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -ms /bin/bash $APP_USER
ENV PATH="${PATH}:/home/$APP_USER/.local/bin"

RUN chown -R $APP_USER:$APP_USER $APP_HOME
USER $APP_USER

COPY . .

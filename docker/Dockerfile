FROM python:3.11-slim

# Evita prompts interativos ao instalar pacotes
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza o sistema e instala dependências para Chrome + netcat
RUN apt-get update && apt-get install -y \
  wget unzip gnupg curl \
  fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
  libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 \
  libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 \
  libxrandr2 xdg-utils libu2f-udev libvulkan1 \
  chromium chromium-driver netcat-openbsd \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Define variável de ambiente para o Chrome Driver
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver
ENV PATH=$CHROMEDRIVER_PATH:$PATH

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Garante permissão de execução para entrypoint
RUN chmod +x docker/entrypoint.sh
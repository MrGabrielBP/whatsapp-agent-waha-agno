FROM python:3.13.5-slim-bookworm AS build

# Instala o curl (necessário para baixar o uv)
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/bin/bash whatsapp_agent

FROM build AS development

USER whatsapp_agent
WORKDIR /home/whatsapp_agent

# Instala o uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# ADICIONE ESTA LINHA: Garante que o container ache o comando 'uv'
ENV PATH="/home/whatsapp_agent/.local/bin:${PATH}"

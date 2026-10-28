FROM ubuntu:latest

# Отключение интерактивных диалогов при установке пакетов
ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем системные зависимости, Python, wget и утилиты
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    wget \
    ca-certificates \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://downloads.dev.extcam.xyz/repository/build_artifacts/desktop-server/master/13622/ivideon/ivideon-video-server_3.16.0-13622~edeb8bd_amd64.deb -O /tmp/ivideon-server.deb \
    && apt-get update \
    && apt-get install -y /tmp/ivideon-server.deb \
    && rm -rf /var/lib/apt/lists/* \
    && rm /tmp/ivideon-server.deb


# Рабочая директория для скриптов
WORKDIR /app

RUN mkdir -p /app/data /app/config

# Скрипт конфигурации и шаблон пустого конфига
COPY change_config_script.py /app/change_config_script.py
COPY tamplate_videoserverd.config /app/tamplate_videoserverd.config
COPY requirements.txt .


RUN pip3 install --no-cache-dir -r requirements.txt

# 554 — стандартный RTSP порт, 8080 — веб-интерфейс Ivideon
EXPOSE 8080 554 443

CMD python3 /app/change_config_script.py && exec /usr/bin/videoserver --config /app/config/videoserverd.config

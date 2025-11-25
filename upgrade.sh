#!/bin/bash
set -euo pipefail

ACTION=${1:-start}
ENV=${2:-dev}

load_env() {
    local env_file=$1
    if [[ -f "$env_file" ]]; then
        set -a
        source "$env_file"
        set +a
    else
        echo "Файл $env_file не найден" >&2
        exit 1
    fi
}

compose_dev_files=(-f docker-compose.yml)
if [[ -f docker-compose.local.yml ]]; then
    compose_dev_files+=(-f docker-compose.local.yml)
fi

case "${ACTION} ${ENV}" in
  "start dev")
    load_env ".env.dev"
    docker-compose --env-file .env.dev "${compose_dev_files[@]}" up -d
    ;;
  "stop dev")
    load_env ".env.dev"
    docker-compose --env-file .env.dev "${compose_dev_files[@]}" down
    ;;
  "start prod")
    load_env ".env.prod"
    docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml up -d
    ;;
  "stop prod")
    load_env ".env.prod"
    docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml down
    ;;
  "renew prod")
    # Обновление/получение сертификата через certbot в Docker
    load_env ".env.prod"

    if [[ -z "${CERTBOT_DOMAINS:-}" || -z "${CERTBOT_EMAIL:-}" ]]; then
        echo "Добавьте CERTBOT_DOMAINS (comma-separated) и CERTBOT_EMAIL в .env.prod" >&2
        exit 1
    fi

    # Убедимся, что папки для certbot существуют
    mkdir -p certbot/conf certbot/www

    # Преобразуем список доменов в аргументы -d
    IFS=',' read -r -a DOMAIN_ARRAY <<< "$CERTBOT_DOMAINS"
    domains_args=""
    for d in "${DOMAIN_ARRAY[@]}"; do
        d_trimmed="$(echo "$d" | xargs)" # trim whitespace
        domains_args+=" -d ${d_trimmed}"
    done

    # Останавливаем nginx чтобы освободить порт 80
    echo "Останавливаем nginx для standalone mode..."
    docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml stop nginx

    # Получение сертификата через standalone mode
    echo "Получение сертификата через standalone mode..."
    docker run --rm \
        -p 80:80 \
        -v "$PWD/certbot/conf:/etc/letsencrypt" \
        -v "$PWD/certbot/www:/var/www/certbot" \
        certbot/certbot certonly \
        --standalone \
        --non-interactive \
        --agree-tos \
        --email "$CERTBOT_EMAIL" \
        ${domains_args}

    # Запускаем nginx обратно
    echo "Запускаем nginx обратно..."
    docker-compose --env-file .env.prod -f docker-compose.yml -f docker-compose.prod.yml start nginx

    echo "Сертификат успешно получен/обновлен!"
    ;;
  "renew-dns prod")
    # Альтернативный способ: DNS verification (не требует остановки nginx)
    load_env ".env.prod"

    if [[ -z "${CERTBOT_DOMAINS:-}" || -z "${CERTBOT_EMAIL:-}" ]]; then
        echo "Добавьте CERTBOT_DOMAINS (comma-separated) и CERTBOT_EMAIL в .env.prod" >&2
        exit 1
    fi

    mkdir -p certbot/conf certbot/www

    IFS=',' read -r -a DOMAIN_ARRAY <<< "$CERTBOT_DOMAINS"
    domains_args=""
    for d in "${DOMAIN_ARRAY[@]}"; do
        d_trimmed="$(echo "$d" | xargs)"
        domains_args+=" -d ${d_trimmed}"
    done

    echo "DNS verification mode - вам нужно будет добавить TXT запись в DNS"
    docker run --rm \
        -v "$PWD/certbot/conf:/etc/letsencrypt" \
        certbot/certbot certonly \
        --manual \
        --preferred-challenges dns \
        --non-interactive \
        --agree-tos \
        --email "$CERTBOT_EMAIL" \
        ${domains_args}
    ;;
  *)
    echo "Использование: ./upgrade.sh [start|stop|renew|renew-dns] [dev|prod]"
    echo "  renew      - Получить/обновить сертификат (standalone mode)"
    echo "  renew-dns  - Получить/обновить сертификат (DNS verification)"
    exit 1
    ;;
esac
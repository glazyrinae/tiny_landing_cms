#!/bin/bash
set -euo pipefail

ACTION=${1:-up}
ENV=${2:-dev}

usage() {
    cat <<'EOF'
Использование: ./upgrade.sh [up|build|stop|ps] [dev|prod]

Команды:
  up     Запустить окружение
  build  Пересобрать образы без кеша
  stop   Остановить окружение
  ps     Показать запущенные контейнеры окружения
EOF
}

load_env() {
    local env_file=$1
    if [[ -f "$env_file" ]]; then
        set -a
        source "$env_file"
        set +a
    else
        echo "Файл $env_file не найден" >&2
        if [[ -f "$env_file.example" ]]; then
            echo "Создайте его из шаблона и заполните значения:" >&2
            echo "  cp $env_file.example $env_file" >&2
        fi
        exit 1
    fi
}

compose() {
    if docker compose version >/dev/null 2>&1; then
        docker compose "$@"
    elif command -v docker-compose >/dev/null 2>&1; then
        docker-compose "$@"
    else
        echo "Docker Compose не найден. Установите Docker Compose v2." >&2
        exit 1
    fi
}

compose_dev_files=(-f docker-compose.yml)
if [[ -f docker-compose.local.yml ]]; then
    compose_dev_files+=(-f docker-compose.local.yml)
fi

compose_prod_files=(-f docker-compose.yml -f docker-compose.prod.yml)

case "$ENV" in
  dev)
    env_file=".env.dev"
    compose_files=("${compose_dev_files[@]}")
    ;;
  prod)
    env_file=".env.prod"
    compose_files=("${compose_prod_files[@]}")
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac

load_env "$env_file"

case "$ACTION" in
  up)
    compose --env-file "$env_file" "${compose_files[@]}" up -d
    ;;
  build)
    compose --env-file "$env_file" "${compose_files[@]}" build --no-cache
    ;;
  stop)
    compose --env-file "$env_file" "${compose_files[@]}" down
    ;;
  ps)
    compose --env-file "$env_file" "${compose_files[@]}" ps
    ;;
  *)
    usage >&2
    exit 1
    ;;
esac

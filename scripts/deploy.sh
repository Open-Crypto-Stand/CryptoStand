#!/bin/bash

ROOT_DIRECTORY="./"

run_docker_compose() {
  local directory=$1
  find "$directory" -type f -name "docker-compose.yml" | while read -r compose_file; do
    compose_dir=$(dirname "$compose_file")
    echo "Запуск docker-compose для: $compose_dir"
    (cd "$compose_dir" && docker-compose up --build -d) || echo "Ошибка при запуске в $compose_dir"
  done
}

run_docker_compose "$ROOT_DIRECTORY"
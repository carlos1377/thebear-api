#!/bin/sh

while ! nc ping -h "localhost" -u "${MYSQL_USER}" -p"${MYSQL_PASSWORD}"; do
  echo "O serviço MySQL não está respondendo. Aguardando... 🕐"
  sleep 10
done
echo "O serviço MySQL está respondendo 🐬"
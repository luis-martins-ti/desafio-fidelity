#!/bin/sh

echo "Esperando o banco Postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Banco disponível!"

# Roda as migrations antes de iniciar o servidor
python manage.py migrate

# Inicia o servidor Django
exec python manage.py runserver 0.0.0.0:8000

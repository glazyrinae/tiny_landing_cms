# Tiny Landing CMS

Tiny Landing CMS is a small Django-based CMS for managing a landing page through
the Django admin panel.

## Stack

- Python 3.12
- Django 5
- PostgreSQL 15
- Docker Compose
- Gunicorn + Nginx for production

## Project Structure

```text
.
|-- app/                    # Django project and apps
|   |-- manage.py
|   |-- tiny_cms/            # Django settings, urls, ASGI/WSGI
|   |-- hero/                # Hero section content
|   |-- about/               # About section content
|   |-- service/             # Services section content
|   |-- price/               # Pricing section content
|   |-- command/             # Team/command section content
|   |-- address/             # Address/contact content
|   `-- settings/            # Global site settings
|-- deploy/                 # Django Docker image and database data
|-- nginx/                  # Production Nginx config
|-- media/                  # Uploaded media files
|-- logs/                   # Application logs
|-- docker-compose.yml      # Base Docker Compose config
|-- docker-compose.local.yml
|-- docker-compose.prod.yml
`-- upgrade.sh              # Helper script for dev/prod compose commands
```

## Requirements

- Docker
- Docker Compose v2 (`docker compose`)

Legacy `docker-compose` v1 can fail on newer Docker versions with
`KeyError: 'ContainerConfig'`. Use Docker Compose v2 commands below.

## Environment Files

Local development uses `.env.dev`.

Production uses `.env.prod`.

## Local Development

Start only the services required for the site:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml up -d db web
```

Apply database migrations:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py migrate
```

Open the site:

```text
http://localhost:8000
```

Open the admin panel:

```text
http://localhost:8000/admin/
```

Create an admin user:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py createsuperuser
```

## Running All Development Services

Use the helper script to start all enabled development services:

```bash
./upgrade.sh start dev
```

Stop development services:

```bash
./upgrade.sh stop dev
```

In the current compose file, the enabled development services are `db` and
`web`.

## Useful Commands

Show running containers:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml ps
```

Follow Django logs:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml logs -f web
```

Open a shell in the Django container:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml exec web sh
```

Run Django checks:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py check
```

Stop local site services:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml down
```

## Production

Before production start, configure `.env.prod`, domain names, Traefik labels,
Nginx config, and the external `traefik-public` Docker network.

Start production services:

```bash
./upgrade.sh start prod
```

Stop production services:

```bash
./upgrade.sh stop prod
```

Certificate helpers:

```bash
./upgrade.sh renew prod
./upgrade.sh renew-dns prod
```

## Common Issues

Port `8000` is already in use.

Stop the process using the port or change the port mapping in
`docker-compose.local.yml`.

Database changes are not applied.

Run migrations:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml exec web python manage.py migrate
```

Warnings like `The "SQL_USER" variable is not set` when viewing logs.

Use the project env file with Compose commands:

```bash
docker compose --env-file .env.dev -f docker-compose.yml -f docker-compose.local.yml logs -f web
```

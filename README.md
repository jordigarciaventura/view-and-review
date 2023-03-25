# view-and-review

## Development

> Use `TAB` for autocomplete and double `TAB` to list commands and containers.

### Docker Compose
Run development containers:
```
docker compose --env-file .env/.env up --build
```

Run production containers:
```
docker compose --env-file .env/.env.prod -f docker-compose.prod.yml up  --build
```

Stop containers:
```
docker compose down
```

Clean volumes (will remove database):
```
docker compose down -v
```

List running containers:
```
docker compose ps
```

Develop inside a running container:
```
docker compose exec <container> bash
```

### PostgreSQL
Access psql:
```
psql -U postgres
```

Common _psql_ commands:
- `\du`: list users
- `\l`: list databases
- `\c <database>`: connect to a database
- `\dt`: list tables 


### Poetry
Add a python package:
```
poetry add <package>
```

### Environment variables
Copy `.env/*template` files without the `.template` suffix.

If you add new variables ensure to add them in the template.

## Design
The development environment has:
- **Web app**: django
- **WSGI**: django built-in
- **Database**: postgreSQL

The production environment has:
- **Web app**: django
- **WSGI**: gunicorn 
- **Database**: postgreSQL
- **Web server**: nginx
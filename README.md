# view-and-review

## Development

> Use `TAB` for autocomplete and double `TAB` to list commands and containers.

### Docker Compose
Build and run:
```
docker compose up --build
```

List running containers:
```
docker compose ps
```

Develop inside a running container:
```
docker compose exec <container> bash
```

Stop and remove services:
```
docker compose down
```

### Poetry
Add a python package:
```
poetry add <package>
```

### Environment variables
Copy [`.env.template`](project/.env.template) as `.env` and feel free to modify it.
If you add new variables ensure to add them to the template.
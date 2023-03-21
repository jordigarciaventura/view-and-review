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

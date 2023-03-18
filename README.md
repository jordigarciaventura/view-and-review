# view-and-review

## Development
### Docker
Build and run a dettached container:
```
docker compose up --build -d
```

Capture logs from the container:
```
docker compose logs -f django
```

Run bash inside the container:
```
docker compose exec django bash
```

### Poetry
Add a python package:
```
poetry add <package>
```

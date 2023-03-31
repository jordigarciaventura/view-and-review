# view-and-review

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/GEI-WP/view-and-review)


## Run Locally

> Copy `secrets/*.template` files without the `.template` suffix.

Development
```
docker compose up --build
```

Production
```
docker compose -f docker-compose.prod.yml up  --build
```

## Design

||Development|Production|
|--|--|--|
| Web app | django | django
| WSGI      | django bulit-in | gunicorn
| Database  | postgreSQL| postgreSQL
| Web Server | -| nginx
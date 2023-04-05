# view-and-review

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/GEI-WP/view-and-review)


## Run Locally

### Development
1. Run the containers:
    ```
    docker compose up --build
    ```
2. Visit http://localhost:8000

### Deployment
1. Run the containers:
    ```
    docker compose -f docker-compose.dep.yml up  --build
    ```
2. Visit http://localhost

### Deployment over HTTPS

1. Install [mkcert](https://github.com/FiloSottile/mkcert#installation)

2. Create a local certificate authority
    ```
    mkcert -install
    ```
3. Create a trusted certificate on `/ngnix/certficates`
    ```
    cd nginx/certificates
    ```
    ```
    mkcert localhost
    ```
4. Run the containers:
    ```
    docker compose -f docker-compose.deps.yml up  --build
    ```
5. Visit https://localhost

## Services

||Development|Deployment|
|--|--|--|
| **Web app** | django | django
| **WSGI**      | django bulit-in | gunicorn
| **Database**  | postgreSQL| postgreSQL
| **Web Server** | -| nginx
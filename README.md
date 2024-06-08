# view-and-review

[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/GEI-WP/view-and-review)


## Run Locally

### Development
1. Copy the `secrets/env.dev.example` file to `secrets/.env.dev` and fill it
2. Run the containers:
    ```
    docker compose up --build
    ```
3. Visit http://localhost:8000

### Deployment
1. Copy the `secrets/env.dep.example` file to `secrets/.env.dep` and fill it
2. Run the containers:
    ```
    docker compose -f docker-compose.dep.yml up --build
    ```
3. Visit http://localhost

### Deployment over HTTPS
1. Copy the `secrets/env.deps.example` file to `secrets/.env.deps` and fill it
   
2. Install [mkcert](https://github.com/FiloSottile/mkcert#installation)

3. Create a local certificate authority
    ```
    mkcert -install
    ```
4. Create a trusted certificate on `/ngnix/certficates`
    ```
    cd nginx/certificates
    ```
    ```
    mkcert localhost
    ```
5. Run the containers:
    ```
    docker compose -f docker-compose.deps.yml up --build
    ```
6. Visit https://localhost

> The deployment over HTTPS uses HSTS policies, so browser will redirect the HTTP requests to HTTPS for security. To delete the policies for localhost in Chrome, for example, go to [chrome://net-internals/#hsts](chrome://net-internals/#hsts) > Domain Security Policy > Delete domain security policies, and add `localhost` to the input field. 

## Services

||Development|Deployment|
|--|--|--|
| **Web app** | django | django
| **WSGI**      | django bulit-in | gunicorn
| **Database**  | postgreSQL| postgreSQL
| **Web Server** | -| nginx
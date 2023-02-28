# Setup

## Docker

**Environment variables**

- `OPENAI_API_KEY` (optional)
- `WEB_IMAGE` (optional), default: `ai-ml-web:latest` - you can skip building your local image and use pre-built
  no-code image `bojanrajh/python:latest`

**Examples**

```bash
$ export OPENAI_API_KEY="sk-..."
$ export WEB_IMAGE="bojanrajh/python:latest"
```

Or prefix `docker stack deploy` / `docker compose` commands with `env WEB_IMAGE="bojanrajh/python:latest"`

Optionally, build local docker image with:

- `python` v3.10
- `poetry` (+ install dependencies)
- `uvicorn` server

```bash
$ docker build -t ai-ml-web:latest -f ./Dockerfile-web .
```

Init docker swarm and deploy stack.

```bash
$ docker swarm init
$ docker stack deploy ai-ml -c docker-compose.yml --prune
```

Or if you would like to use standard non-swarm docker compose:

```bash
$ docker compose up
```

Or if you would like to manually run a single container:

```bash
$ docker run -dit \
 -p 10002:80 \
 -v "$PWD:/code" \
 -v "$PWD/data:/data/docs" \
 -v "$PWD/db:/data/db" \
 -v "$PWD:/cache:/data/cache" \
 ai-ml-web:latest
```

Open your browser: [http://172.18.0.1:10002/](http://172.18.0.1:10002/)
or [http://localhost:10002/](http://localhost:10002/)

If above links do not work, check IPs returned by the command:

```bash
$ docker container exec -it $(docker ps -f name=ai-ml_web --format "{{.ID}}") hostname -I
```

Run tests

```bash
$ docker container exec -it $(docker ps -f name=ai-ml_web --format "{{.ID}}") pytest
```

## Local

Install dependencies with poetry.

```bash
$ poetry install
```

Enter isolated poetry shell.

```bash
$ poetry shell
```

Run uvicorn web server.

```bash
$ uvicorn web.main:app --host 0.0.0.0 --port 80 --reload
```

## Devenv

Activate direnv from your project root:

```bash
$ direnv allow
```

Run uvicorn web server.

```bash
$ uvicorn web.main:app --host 0.0.0.0 --port 80 --reload
```

# Endpoint examples

## Upload input

Upload .zip containing .md files.

```bash
$ curl -v -F content=@test.zip https://ai-ml.fly.dev/upload-input
```

Or with custom collection.

```bash
$ curl \
 -v \
 -F content=@test.zip \
 -F collection=test \
 https://ai-ml.fly.dev/upload-input
```

## Ingestion

Ingest uploaded documents.

```bash
$ curl -X POST https://ai-ml.fly.dev/ingest
```

Or with custom collection.

```bash
$ curl \
 -X POST \
 --data '{"collection":"test"}' \
 --header "Content-Type: application/json" \
 https://ai-ml.fly.dev/ingest
```

## Search

Search default collection.

```bash
$ curl \
 -X POST \
 --header "Content-Type: application/json" \
 --data '{"query":"keywords"}' \
 https://ai-ml.fly.dev/query
```

Search custom collection.

```bash
$ curl \
 -X POST \
 --header "Content-Type: application/json" \
 --data '{"query":"keywords","collection":"test"}' \
 https://ai-ml.fly.dev/query
```

# Notes

Notes:

- auto-reload is supported with `--reload` parameter in the `uvicorn` entrypoint

Fly.io deployment:

- See [./.github/workflows/test.yml](./.github/workflows/test.yml)
- `fly auth docker --access-token ...`
- `fly deploy -i ai-ml-server:latest` - push local image to fly.io, then deploy
- `fly secrets set OPENAI_API_KEY="..."` - or fallback to tensorflow
- `fly volumes create data --region ams --size 1` + see [./fly-toml](./fly-toml)
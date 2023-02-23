# Docker

Build docker image with:
 - `python` v3.10
 - `poetry` (+ install dependencies)
 - `uvicorn` server

```bash
$ docker build -t ai-ml-web -f ./Dockerfile-web .
```

Init docker swarm and deploy stack.

```bash
$ docker swarm init
$ docker stack deploy ai-ml -c docker-compose.yml --prune
```

Open your browser: [http://172.18.0.1:10002/](http://172.18.0.1:10002/) or [http://localhost:10002/](http://localhost:10002/) 

Run tests
```bash
$ docker container exec -it $(docker ps -f name=ai-ml_web --format "{{.ID}}") pytest
```

# Local

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
uvicorn web.main:app --host 0.0.0.0 --port 80 --reload
```

# Devenv?

# Notes

Notes:
 - auto-reload is supported with `--reload` parameter in the `uvicorn` entrypoint

Fly.io deployment:
 - See [./.github/workflows/test.yml](./.github/workflows/test.yml)
 - `fly auth docker --access-token YmXTfdnd82-t1dedLsi48tx_bJzczU2NNivei_zcxkk`
 - `fly deploy -i ai-ml-server:latest`
 - `fly secrets set OPENAI_API_KEY="..."`
 - `fly volumes create input_docs --region ams --size 1` + see [./fly-toml](./fly-toml)
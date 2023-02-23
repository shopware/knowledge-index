Build docker image with:
 - `python` v3.10
 - `poetry` (+ install dependencies)
 - run `uvicorn` server

```bash
$ docker build -t ai-ml-server -f ./Dockerfile .
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

Notes:
 - auto-reload is supported with `--reload` parameter in the `uvicorn` entrypoint
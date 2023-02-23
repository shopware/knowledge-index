Build docker image.

```bash
$ docker build -t ai-ml-server -f ./Dockerfile .
```

Deploy docker stack.

```bash
$ docker stack deploy ai-ml -c docker-compose.yml --prune
```

Open your browser: [http://172.18.0.1:10001/](http://172.18.0.1:10001/)

Run tests
```bash
$ docker container exec -it $(docker ps -f name=ai-ml_ai-ml --format "{{.ID}}") pytest
```

Notes:
 - auto-reload is supported with `--reload` parameter in the `uvicorn` entrypoint
 - deploy to platform.sh: `git push -u platform main`
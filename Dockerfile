FROM python:3.9

#RUN curl -L https://fly.io/install.sh | sh

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

# add --proxy-headers when running behind proxy
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

# gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
# uvicorn main:app --host 0.0.0.0 --port 8080 --workers 4

# run image with "docker build -t ai-ml-server ."
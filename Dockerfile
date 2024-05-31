FROM public.ecr.aws/docker/library/python
COPY ./app /app

WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT gunicorn app:get_app --worker-class aiohttp.GunicornWebWorker --bind 0.0.0.0:8080
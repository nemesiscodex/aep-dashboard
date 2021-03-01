FROM python:3.9.2-slim
RUN apt-get update -qq && apt-get install -y pkg-config openssl libssl-dev libpq-dev binutils libproj-dev gdal-bin gcc cron && rm -rf /var/lib/apt/lists/*
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

ADD . /app/

CMD [ "sh", "/app/run.sh" ]
From python:3.8

WORKDIR /app

ENV TELEGRAM_TOKEN=${TELEGRAM_TOKEN}
ENV MINIO_ROOT_USER=${MINIO_ROOT_USER}
ENV MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
ENV HOST_PORT=${HOST_PORT}

COPY . ./app
RUN mkdir -p .app/temp
RUN pip install -r ./app/requirements.txt

CMD ["python", "./app/src/bot.py"]
From python:3.8

WORKDIR /src/app

COPY . /src/app

RUN pip install -r requirements.txt

CMD ["python", "./src/main.py"]
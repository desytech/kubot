FROM python:3.8-alpine

RUN pip install --upgrade pip

RUN apk --update add gcc musl-dev postgresql-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "kubot.py"]
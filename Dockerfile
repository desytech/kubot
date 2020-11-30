FROM python:3.8-alpine

RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "kubot.py"]
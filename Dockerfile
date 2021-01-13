FROM python:3.8-alpine as base

RUN pip install --upgrade pip

RUN apk --update add gcc musl-dev postgresql-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

FROM base as development
CMD ["python", "src/kubot.py"]

FROM base as production
ADD http://pyarmor.dashingsoft.com/downloads/latest/alpine/_pytransform.so /usr/local/lib/python3.8/site-packages/pyarmor/platforms/linux/x86_64/
RUN pyarmor obfuscate --exclude venv --exclude tests --recursive src/kubot.py
RUN rm -rf src
CMD ["python", "dist/kubot.py"]


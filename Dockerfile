FROM python:3.13-alpine as base

RUN pip install --upgrade pip

RUN apk --update add gcc musl-dev postgresql-dev git

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

FROM base as development
CMD ["./wait-for", "postgres:5432", "--", "python", "src/kubot.py"]

FROM base as production
ARG TARGETPLATFORM
RUN if [ "$TARGETPLATFORM" = "linux/amd64" ] ; then wget -O /usr/local/lib/python3.8/site-packages/pyarmor/platforms/linux/x86_64/_pytransform.so http://pyarmor.dashingsoft.com/downloads/latest/alpine/_pytransform.so ; fi
RUN if [ "$TARGETPLATFORM" = "linux/arm/v7" ] ; then mkdir -p /root/.pyarmor/platforms/linux/armv7/3/ && wget -O /root/.pyarmor/platforms/linux/armv7/3/_pytransform.so http://pyarmor.dashingsoft.com/downloads/latest/alpine.arm/_pytransform.so ; fi

RUN pyarmor obfuscate --exclude venv --exclude tests --recursive src/kubot.py
RUN rm -rf src
CMD ["./wait-for", "postgres:5432", "--", "python", "dist/kubot.py"]


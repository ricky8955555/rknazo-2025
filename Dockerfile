# Build

FROM python:3.12-alpine3.21 AS build

WORKDIR /rknazo
COPY src/ .

RUN apk add --update --no-cache git
RUN pip install -r requirements.txt

RUN python3 build.py


# Configure environment

FROM python:3.12-alpine3.21 AS environ

WORKDIR /rknazo
COPY --from=build /rknazo/out .
COPY src/environ/ ./environ

RUN apk add --update --no-cache git
RUN pip install -r requirements.txt

RUN python3 configure.py
RUN rm configure.py requirements.txt

RUN find . -type d -name __pycache__ -delete
RUN rm -r /root/.cache


# Flatten layers

FROM python:3.12-alpine3.21

COPY --from=environ / /

WORKDIR /rknazo

ENTRYPOINT [ "python3", "run.py" ]

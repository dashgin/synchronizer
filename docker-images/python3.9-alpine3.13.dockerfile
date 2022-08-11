FROM python:3.10-alpine3.13

LABEL maintainer="Dashgin Khudiyev <xudiyevdasqin77777@gmail.com>"

COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache --virtual .build-deps gcc libc-dev \
    && pip install --no-cache-dir -r /tmp/requirements.txt \
    && apk del .build-deps gcc libc-dev


COPY ./ /app
WORKDIR /app/

ENV PYTHONPATH=/app

CMD ["python", "main.py"]

FROM python:3.8.6-alpine3.12 as base 
FROM base as builder

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev

RUN apk add --no-cache mariadb-dev
RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
COPY ./requirements/local.txt /app/requirements.txt

RUN pip install --no-cache-dir --user -r /app/requirements.txt 

WORKDIR /app

FROM base
ENV PYTHONUNBUFFERED 1
RUN apk add --no-cache bash curl
RUN apk add --no-cache mariadb-dev
RUN apk add --no-cache mysql-client
RUN apk add --no-cache libxml2 libxslt
RUN apk add --no-cache libjpeg
COPY --from=builder /root/.local /usr/local
COPY ./ /app
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/gunicorn.sh

WORKDIR /app

ENTRYPOINT ["/app/entrypoint.sh"]

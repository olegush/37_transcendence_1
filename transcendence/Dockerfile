FROM python:3.6.8-alpine
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk add --virtual .build-deps \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    openssl-dev \
    libffi-dev \
    libsodium-dev \
    build-base\
    && pip install psycopg2 && pip install pynacl && pip install cryptography --no-binary cryptography \
    && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
COPY . /usr/src/app/
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

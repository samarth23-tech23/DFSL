FROM alpine:3.16.0

WORKDIR /app

COPY . .
RUN rm -rf nginx .git
RUN rm -f Dockerfile docker-compose.yaml .env README.md .gitignore

RUN apk add --no-cache python3 py3-pip;
RUN apk add postgresql14

RUN pip3 install -r requirements.txt

RUN addgroup -g 1000 appuser;
RUN adduser -u 1000 -G appuser -D -h /app appuser;
RUN chown -R appuser:appuser /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app/static
RUN python3 manage.py collectstatic --noinput

USER appuser
EXPOSE 8000

ENTRYPOINT [\
                "sh",\
                "-c",\
                "python3 manage.py makemigrations; \
                python3 manage.py migrate; \
                python3 manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL; \
                gunicorn --bind 0.0.0.0:8000 DFSL.wsgi:application;"\
            ]

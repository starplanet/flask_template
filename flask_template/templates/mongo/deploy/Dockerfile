FROM python:3.6.6

COPY ./deploy/aliyun.list /etc/apt/sources.list
COPY ./deploy/pip.conf /etc/pip.conf
COPY ./requirements.txt /env/requirements.txt
RUN pip install -r /env/requirements.txt

WORKDIR /app
ADD . /app

ENV WORD_EXTENSION_ENV prod
ENV C_FORCE_ROOT yes
ENV TZ Asia/Shanghai

RUN mkdir -p /data/logs/project_name

CMD gunicorn -c gunicorn_conf_docker.py wsgi:app

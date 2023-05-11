FROM --platform=$BUILDPLATFORM python:3.10 AS builder

WORKDIR /service

COPY requirements.txt /service

RUN apt update
RUN pip install pip --upgrade
RUN pip install -r requirements.txt

COPY . /service

# 환경변수, 앱의 이름은 flask run 명령시 자동 인식하는 이름이므로 생략
ENV FLASK_APP app.py
ENV FLASK_ENV development
ENV FLASK_RUN_PORT 8080
ENV FLASK_RUN_HOST 0.0.0.0

EXPOSE 8080

# 구동 명령
ENTRYPOINT [ "flask", "run"]
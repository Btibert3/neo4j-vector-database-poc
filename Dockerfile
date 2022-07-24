FROM python:3.9-slim-buster

WORKDIR /brock/devenv/

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /brock

ENTRYPOINT [ "bash" ]
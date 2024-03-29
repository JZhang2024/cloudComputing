# syntax=docker/dockerfile:1
FROM python:3.11-slim-bookworm
WORKDIR /
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "main.py" ]
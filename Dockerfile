FROM python:3.10.13-slim

ENV PYTHONBUFFERED=1

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD

EXPOSE 8000
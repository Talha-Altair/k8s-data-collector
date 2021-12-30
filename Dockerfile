FROM python:3.9.5-slim-buster

RUN apt update

RUN apt install stress

ADD ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ADD . .

EXPOSE 9000

CMD [ "python3", "app.py" ]
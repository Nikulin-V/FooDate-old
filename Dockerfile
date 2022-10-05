FROM python:3.9-alpine
MAINTAINER Nikulin Vasily 'nikulin.vasily.777@ya.ru'

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBEFFERED 1

WORKDIR /code

RUN apk --update add
RUN pip install --upgrade pip

COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py migrate && python manage.py collectstatic --no-input
CMD python manage.py runserver 0.0.0.0:8001

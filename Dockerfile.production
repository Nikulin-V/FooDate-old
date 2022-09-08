FROM python:3-alpine
MAINTAINER Nikulin Vasily 'nikulin.vasily.777@ya.ru'

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 445

CMD python manage.py migrate && python manage.py runserver 0.0.0.0:445 --insecure

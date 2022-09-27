FROM tiangolo/uwsgi-nginx
MAINTAINER Nikulin Vasily 'nikulin.vasily.777@ya.ru'

ENV UWSGI_INI /code/django.ini
COPY dev.foodate /etc/nginx/sites-enabled
CMD service nginx restart

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 446

CMD python manage.py migrate && python manage.py collectstatic --no-input
CMD uwsgi --ini django.ini

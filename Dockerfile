FROM tiangolo/uwsgi-nginx
MAINTAINER Nikulin Vasily 'nikulin.vasily.777@ya.ru'

ENV UWSGI_INI /code/dev.foodate.ini
COPY dev.foodate.nginxconf /etc/nginx/sites-enabled

WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt

COPY . /code

EXPOSE 446

CMD python manage.py migrate && python manage.py collectstatic --no-input
CMD gunicorn foodate.wsgi:application --bind 0.0.0.0:446

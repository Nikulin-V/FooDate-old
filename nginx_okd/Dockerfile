FROM nginx:latest
MAINTAINER Nikulin Vasily 'vasil1y.nikulin@ya.ru'
LABEL io.openshift.expose-services="8080:http"

COPY /configs /etc/nginx/conf.d
RUN chmod -R 777 /var/log/nginx /var/cache/nginx /var/run
RUN chgrp -R 0 /etc/nginx
RUN chmod -R g=u /etc/nginx

EXPOSE 8080

FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY certs/todogest.key /etc/ssl/private/todogest.key
COPY certs/todogest.crt /etc/ssl/certs/todogest.crt
RUN mkdir -p /var/log/nginx/healthd
RUN chown -R nginx:nginx /var/log/nginx/healthd
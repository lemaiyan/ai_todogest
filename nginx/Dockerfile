FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir -p /var/log/nginx/healthd
RUN chown -R nginx:nginx /var/log/nginx/healthd
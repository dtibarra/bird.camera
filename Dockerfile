FROM nginx:mainline-alpine

# Install cron and supervisor
RUN apk add --update --no-cache supervisor python3 py3-pip ffmpeg py3-requests && mkdir -p /var/www/html/stream 

# Add supervisor config
COPY config/supervisord.conf /etc/supervisord.conf

# Copy your crontab file
COPY config/crontab /etc/crontabs/root

COPY config/nginx.conf /etc/nginx/conf.d/default.conf

COPY bin/get_curr_weather.py /root/

ADD dist /var/www/html
EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

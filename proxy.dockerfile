FROM ubuntu:focal

RUN apt-get update || true && apt-get install -y nginx openssl

RUN unlink /etc/nginx/sites-enabled/default

RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# COPY ssl_certs/fullchain.pem /etc/ssl/certs/
# COPY ssl_certs/privkey.pem /etc/ssl/private/

COPY ./backendAPI/ /home/backendAPI
COPY ./nginx/nginx.conf /etc/nginx/conf.d/onefi.app.conf

EXPOSE 80/tcp
CMD ["nginx", "-g", "daemon off;"]
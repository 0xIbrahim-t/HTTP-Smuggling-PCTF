FROM nginx:1.21

# Install OpenSSL for certificate generation
RUN apt-get update && apt-get install -y openssl

# Generate self-signed certificates
RUN mkdir -p /etc/nginx/certs && \
    openssl req -x509 -nodes -days 365 \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
    -newkey rsa:2048 -keyout /etc/nginx/certs/nginx.key \
    -out /etc/nginx/certs/nginx.crt

COPY nginx.conf /etc/nginx/nginx.conf
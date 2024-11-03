#!/bin/bash
mkdir -p /etc/apache2/certs
openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/apache2/certs/apache.key \
    -out /etc/apache2/certs/apache.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,DNS:webserver,IP:127.0.0.1"

# Set proper permissions for keys
chmod 600 /etc/apache2/certs/apache.key
chmod 644 /etc/apache2/certs/apache.crt
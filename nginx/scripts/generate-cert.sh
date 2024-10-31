#!/bin/bash

# Check if certificates already exist
if [ ! -f /etc/nginx/cert/cert.pem ] || [ ! -f /etc/nginx/cert/key.pem ]; then
    echo "Generating self-signed certificates..."
    
    # Generate private key and certificate
    openssl req -x509 \
        -nodes \
        -days 365 \
        -newkey rsa:2048 \
        -keyout /etc/nginx/cert/key.pem \
        -out /etc/nginx/cert/cert.pem \
        -subj "/C=US/ST=State/L=City/O=CTF Challenge/CN=localhost" \
        -addext "subjectAltName=DNS:localhost,DNS:*.localhost"

    echo "Certificates generated successfully"
else
    echo "Certificates already exist, skipping generation"
fi

chmod 644 /etc/nginx/cert/cert.pem
chmod 600 /etc/nginx/cert/key.pem
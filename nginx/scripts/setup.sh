#!/bin/bash

# Create cache directory if it doesn't exist
mkdir -p /var/cache/nginx/cache
chmod 700 /var/cache/nginx/cache

# Check if we need to generate certificates
/etc/nginx/scripts/generate-cert.sh

# Start nginx in foreground
echo "Starting nginx..."
nginx -g 'daemon off;'
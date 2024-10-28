FROM nginx:1.21

# Install OpenSSL
RUN apt-get update && apt-get install -y openssl && rm -rf /var/lib/apt/lists/*

# Copy configuration and certificate generation script
COPY nginx.conf /etc/nginx/nginx.conf
COPY generate-certs.sh /docker-entrypoint.d/

# Make the script executable
RUN chmod +x /docker-entrypoint.d/generate-certs.sh

# Update Nginx config to use current syntax
COPY nginx.conf /etc/nginx/nginx.conf
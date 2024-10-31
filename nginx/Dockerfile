FROM nginx:1.21-alpine

# Install required packages
RUN apk add --no-cache openssl bash

# Create directories
RUN mkdir -p /etc/nginx/cert
RUN mkdir -p /var/cache/nginx/cache
RUN mkdir -p /etc/nginx/scripts

# Copy configuration files
COPY nginx.conf /etc/nginx/nginx.conf
COPY scripts/generate-cert.sh /etc/nginx/scripts/
COPY scripts/setup.sh /etc/nginx/scripts/

# Set permissions
RUN chmod +x /etc/nginx/scripts/generate-cert.sh
RUN chmod +x /etc/nginx/scripts/setup.sh

# Generate certificate if not mounted
RUN /etc/nginx/scripts/generate-cert.sh

# Use setup script as entrypoint
ENTRYPOINT ["/etc/nginx/scripts/setup.sh"]
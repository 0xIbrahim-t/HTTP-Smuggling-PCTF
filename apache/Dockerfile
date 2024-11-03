# /apache/Dockerfile
FROM httpd:2.4

# Install required packages
RUN apt-get update && apt-get install -y \
    openssl \
    apache2-dev \
    libapr1-dev \
    libaprutil1-dev \
    lua5.3 \
    liblua5.3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy configurations
COPY httpd.conf /etc/apache2/httpd.conf
COPY cache_control.lua /etc/apache2/cache_control.lua
COPY generate-certs.sh /usr/local/bin/

# Create necessary directories
RUN mkdir -p /etc/apache2/certs /var/cache/apache2 \
    && chmod +x /usr/local/bin/generate-certs.sh

# Generate self-signed certificates
RUN /usr/local/bin/generate-certs.sh

# Set proper permissions
RUN chown -R www-data:www-data /var/cache/apache2

# Expose ports
EXPOSE 443

# Start Apache
CMD ["httpd", "-D", "FOREGROUND"]
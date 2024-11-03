# Use the official Apache HTTP Server image
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

# Copy the Apache configuration files and scripts
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY cache_control.lua /usr/local/apache2/conf/cache_control.lua
COPY generate-certs.sh /usr/local/bin/generate-certs.sh

# Create necessary directories and set permissions
RUN mkdir -p /usr/local/apache2/certs /usr/local/apache2/cache \
    && chmod +x /usr/local/bin/generate-certs.sh \
    && chown -R www-data:www-data /usr/local/apache2/cache

# Generate self-signed certificates
RUN /usr/local/bin/generate-certs.sh

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Start Apache in the foreground
CMD ["httpd", "-D", "FOREGROUND"]

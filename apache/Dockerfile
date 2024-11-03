FROM httpd:2.4

# Install required packages
RUN apt-get update && apt-get install -y \
    openssl \
    libapache2-mod-http2 \
    libapache2-mod-lua \
    lua5.2 \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /etc/apache2/certs \
    && mkdir -p /etc/apache2/lua \
    && mkdir -p /var/cache/apache2 \
    && chown www-data:www-data /var/cache/apache2

# Copy configurations
COPY 000-default.conf /etc/apache2/sites-available/
COPY apache2.conf /etc/apache2/
COPY cache_control.lua /etc/apache2/lua/
COPY generate-certs.sh /usr/local/bin/

# Make scripts executable
RUN chmod +x /usr/local/bin/generate-certs.sh

# Enable required modules
RUN a2enmod ssl proxy proxy_http proxy_http2 http2 cache cache_disk headers rewrite env lua

EXPOSE 80 443

# Use generate-certs.sh as an entry point script
ENTRYPOINT ["sh", "-c", "/usr/local/bin/generate-certs.sh && httpd-foreground"]
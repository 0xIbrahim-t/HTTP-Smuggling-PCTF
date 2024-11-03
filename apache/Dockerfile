FROM httpd:2.4

# Install required packages
RUN apt-get update && apt-get install -y \
    openssl \
    lua5.2 \
    liblua5.2-0 \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p /etc/apache2/certs \
    && mkdir -p /etc/apache2/lua \
    && mkdir -p /var/cache/apache2 \
    && chown www-data:www-data /var/cache/apache2

# Copy configurations
COPY 000-default.conf /usr/local/apache2/conf/extra/
COPY httpd.conf /usr/local/apache2/conf/
COPY cache_control.lua /etc/apache2/lua/
COPY generate-certs.sh /usr/local/bin/

# Make scripts executable
RUN chmod +x /usr/local/bin/generate-certs.sh

# Load modules
RUN sed -i \
    -e 's/#\(LoadModule proxy_module modules\/mod_proxy.so\)/\1/' \
    -e 's/#\(LoadModule proxy_http_module modules\/mod_proxy_http.so\)/\1/' \
    -e 's/#\(LoadModule proxy_http2_module modules\/mod_proxy_http2.so\)/\1/' \
    -e 's/#\(LoadModule ssl_module modules\/mod_ssl.so\)/\1/' \
    -e 's/#\(LoadModule socache_shmcb_module modules\/mod_socache_shmcb.so\)/\1/' \
    -e 's/#\(LoadModule http2_module modules\/mod_http2.so\)/\1/' \
    -e 's/#\(LoadModule cache_module modules\/mod_cache.so\)/\1/' \
    -e 's/#\(LoadModule cache_disk_module modules\/mod_cache_disk.so\)/\1/' \
    -e 's/#\(LoadModule headers_module modules\/mod_headers.so\)/\1/' \
    -e 's/#\(LoadModule rewrite_module modules\/mod_rewrite.so\)/\1/' \
    -e 's/#\(LoadModule lua_module modules\/mod_lua.so\)/\1/' \
    /usr/local/apache2/conf/httpd.conf

# Include extra configurations
RUN echo "Include conf/extra/000-default.conf" >> /usr/local/apache2/conf/httpd.conf

EXPOSE 80 443

# Use generate-certs.sh as an entry point script
ENTRYPOINT ["sh", "-c", "/usr/local/bin/generate-certs.sh && httpd-foreground"]
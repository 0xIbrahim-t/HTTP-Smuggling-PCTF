# Use the official Apache HTTP Server image
FROM httpd:2.4

# Install required packages
RUN apt-get update && apt-get install -y \
    apache2-dev \
    libapr1-dev \
    libaprutil1-dev \
    lua5.3 \
    liblua5.3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the Apache configuration files and Lua script
COPY httpd.conf /usr/local/apache2/conf/httpd.conf
COPY cache_control.lua /usr/local/apache2/conf/cache_control.lua

# Create cache directory and set permissions
RUN mkdir -p /usr/local/apache2/cache \
    && chown -R www-data:www-data /usr/local/apache2/cache

# Expose HTTP port only
EXPOSE 80

# Start Apache in the foreground
CMD ["httpd", "-D", "FOREGROUND"]
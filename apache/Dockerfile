# Use the official Apache HTTP Server image
FROM httpd:2.4

# Install required packages
RUN apt-get update && apt-get install -y \
    apache2-dev \
    libapr1-dev \
    libaprutil1-dev \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories and set permissions
RUN mkdir -p /usr/local/apache2/cache \
    && mkdir -p /usr/local/apache2/logs \
    && chown -R www-data:www-data /usr/local/apache2/cache \
    && chown -R www-data:www-data /usr/local/apache2/logs \
    && chown -R www-data:www-data /usr/local/apache2/htdocs

# Copy the Apache configuration
COPY httpd.conf /usr/local/apache2/conf/httpd.conf

# Expose HTTP port
EXPOSE 80

# Start Apache in the foreground
CMD ["httpd", "-D", "FOREGROUND"]
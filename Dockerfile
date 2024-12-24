FROM alpine:latest

# Install required packages
RUN apk update
RUN apk --no-cache add squid tzdata bash vim  && rm -rf /var/cache/apk/*

# Set timezone
ENV TZ=America/Denver
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create startup script
COPY start-squid.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start-squid.sh

# Create necessary directories
RUN mkdir -p /var/spool/squid /var/log/squid && \
    chown -R squid:squid /var/spool/squid && \
    chown -R squid:squid /var/log/squid

# # Copy configuration
# COPY squid.conf /etc/squid/squid.conf
# RUN chmod 644 /etc/squid/squid.conf

# Expose port
EXPOSE 3128

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD squidclient cache_object://localhost mgr:info || exit 1

# Use the startup script as entrypoint
ENTRYPOINT ["/usr/local/bin/start-squid.sh"]
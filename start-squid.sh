#!/bin/bash

# Initialize cache directory if it doesn't exist
if [ ! -d /var/spool/squid/00 ]; then
    echo "Initializing cache directories..."
    squid -z -f /etc/squid/squid.conf

    # Wait for initialization to complete
    sleep 5
fi

# Check if initialization was successful
if [ ! -d /var/spool/squid/00 ]; then
    echo "Cache directory initialization failed!"
    exit 1
fi

# Start Squid in non-daemon mode with debug level 1
exec squid -f /etc/squid/squid.conf -NYCd 1


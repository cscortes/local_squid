FROM alpine:latest
EXPOSE 3128/tcp 

RUN apk update && apk add squid bash vim 

RUN mkdir -p /cache && \ 
    chown -R squid:squid /cache && \ 
    chown -R squid:squid /var/log/squid 
 
#
COPY squid.conf /etc/squid 
RUN echo "Initializing cache..." && \
    rm -rf /var/run/squid* && \ 
    /usr/sbin/squid -N -f /etc/squid/squid.conf -z \
    @echo done creating cache 

CMD [ "/usr/sbin/squid", "-N",  "-d", "1" ]

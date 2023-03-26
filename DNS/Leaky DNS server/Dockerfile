# docker build --tag be .
# docker run --privileged -d -p 53:53/udp -p 53:53 be

FROM centos:centos8

MAINTAINER <thomas.dupas@dnsbelgium.be>

COPY build-scripts/prepare_container.sh /tmp/prepare_container.sh
COPY build-scripts/start_named.sh /tmp/start_named.sh
COPY config/named.conf /etc/named.conf

RUN chmod +x /tmp/prepare_container.sh
RUN /tmp/prepare_container.sh

COPY --chown=named:named config/be.zone.unsigned /var/named/dynamic/be/be.zone

EXPOSE 53/udp 53/tcp

RUN chmod +x /tmp/start_named.sh
ENTRYPOINT /tmp/start_named.sh

#Demo file  should not use in production should import known trusted rpm keys

#FROM registry.access.redhat.com/ubi8/ubi
FROM docker.io/rockylinux:8

MAINTAINER <support@dnsbelgium.be>

COPY buildscripts /tmp/buildscripts
RUN chmod +x /tmp/buildscripts/prepare_container_nsd.sh
RUN /tmp/buildscripts/prepare_container_nsd.sh

COPY application/application_nsd.sh /usr/local/bin/application.sh
RUN chmod +x /usr/local/bin/application.sh

#use this docker as an executable
#http://goinbigdata.com/docker-run-vs-cmd-vs-entrypoint/
# As everything is passed to the entrypoint, you can have a very nice behavior from your images.
# @Jiri example is good, it shows how to use an image as a "binary". When using ["/bin/cat"] as entrypoint and then doing docker run img /etc/passwd, you get it,
# /etc/passwd is the command and is passed to the entrypoint so the end result execution is simply /bin/cat /etc/passwd.

#Default argument for ENTRYPOINT if no argument is given at docker run
#For reference, for this container it is not needed
#CMD [ "defaultarugment" ]
CMD ["/usr/local/bin/application.sh"]


#To debug an entrypoint container exec a shell in it or overwrite entrypoint during start
#docker run -it --entrypoint /bin/sh container
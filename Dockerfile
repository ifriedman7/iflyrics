###############################################################################
# Dockerfile for iflyrics
###############################################################################

#FROM alpine:3
FROM python:3.8.10-alpine
#apache2 apache2-utils python3 py3-pip openrc
RUN apk --update --no-cache add alpine-sdk libxml2-dev curl-dev git bash; \
    rm -rf /var/cache/apk/*; 

RUN git clone https://github.com/ifriedman7/iflyrics
WORKDIR iflyrics
RUN pip3 install -r requirements.txt


# Set default command
#CMD ["/usr/bin/bash"]
EXPOSE 3001
ENTRYPOINT [ "python3", "query_app.py" ]

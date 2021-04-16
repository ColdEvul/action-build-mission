FROM arwynfr/armake2:alpine

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY ./entrypoint.sh /entrypoint.sh
COPY tools /tools
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
FROM arwynfr/armake2:alpine as base

FROM alpine:3

COPY --from=base /usr/bin/armake2 /usr/bin/armake

# Install python/pip
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

COPY ./entrypoint.sh /entrypoint.sh
COPY tools /tools
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
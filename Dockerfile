FROM alpine:3.5

COPY . /root/

RUN apk add --update \
    python \
    python-dev \
    py-pip \
  && pip install --requirement /root/requirements.txt \
  && rm -rf /var/cache/apk/*

WORKDIR /root/

EXPOSE 5000

CMD ["/usr/bin/python", "app.py"]
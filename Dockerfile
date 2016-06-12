FROM python:2-alpine

# default scrapy profile
ENV SCRAPY_PROFILE dev

RUN mkdir -p /tmp/scraper \
    && apk update \
    && apk add --no-cache \
        gcc \
        libxml2-dev \
        libxslt-dev \
        libc-dev \
        libffi-dev \
        openssl-dev \
        libtirpc-dev \
    && ln -s /usr/include/tirpc/rpc /usr/include/rpc \
    && ln -s /usr/include/tirpc/netconfig.h /usr/include/netconfig.h \
    && pip install --no-cache-dir service-identity

COPY . /tmp/scraper/

RUN cd /tmp/scraper \
    && python setup.py install \
    && rm -Rf ~/.cache /tmp/scraper

CMD ["/usr/local/bin/scraperd", "-n"]
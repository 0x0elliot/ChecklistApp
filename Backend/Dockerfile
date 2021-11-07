FROM ubuntu:latest
WORKDIR /opt/API

COPY . /opt/API

RUN chmod +x docker-entrypoint.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
	    python3-pip \
        git

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "/opt/API/docker-entrypoint.sh" ]
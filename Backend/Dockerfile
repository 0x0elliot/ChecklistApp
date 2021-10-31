FROM ubuntu:latest
WORKDIR /opt/API

COPY . /opt/API

RUN chmod +x /opt/API/docker-entrypoint.sh

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
	    python3-pip \
        git

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=manager.py


CMD ["python3", "manager.py", "runserver"]
FROM debian:stable-slim

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install -y python3 python3-pip

COPY *.py requirements.txt /app/
WORKDIR /app

RUN pip install -r requirements.txt

# We need to run as root in order to access the docker socket
# with --userns host

EXPOSE 8080
CMD uwsgi --need-app --http :8080 --wsgi-file wsgi.py --callable app

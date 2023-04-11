
FROM python:3.8-slim-buster

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ARG DEBIAN_FRONTEND=noninteractive

# Install Firefox binary
RUN apt-get update && \
    apt-get install -y firefox-esr --no-install-recommends && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata 

# Install pip requirements
WORKDIR /app

COPY requirements.txt  ./
RUN python -m pip install --upgrade pip 
RUN python -m pip install -r requirements.txt
RUN python -m pip install pyopenssl==22.0.0

COPY . ./

ENTRYPOINT [ "/bin/sh" ]
CMD [ "./entrypoint.sh" ]

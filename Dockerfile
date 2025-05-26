# Use an official Python runtime as a parent image
FROM python:3.10-slim

RUN apt-get update
RUN apt install -y rsync curl

# create dirs
RUN mkdir -p /data/pub
RUN mkdir /data/temp

# Copy application code into the container
COPY download_and_search.py /data
COPY upd_alboge_channel_async.py /data
COPY upd_cippt_channel.py /data
COPY requirements.txt /data

# Set the working directory in the container
WORKDIR /data

# Install dependencies
RUN pip install setuptools pip wheel --upgrade
RUN pip install -r requirements.txt

# kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x kubectl
RUN mv kubectl /usr/local/bin/

COPY krsync.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/krsync.sh


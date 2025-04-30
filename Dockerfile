# Use an official Python runtime as a parent image
FROM python:3.10-slim

RUN apt-get update
RUN apt install -y rsync

# create dirs
RUN mkdir -p /data/pub
RUN mkdir /data/temp

# Copy application code into the container
COPY download_and_search.py /data
COPY requirements.txt /data

# Set the working directory in the container
WORKDIR /data

# Install dependencies
RUN pip install setuptools pip wheel --upgrade
RUN pip install -r requirements.txt

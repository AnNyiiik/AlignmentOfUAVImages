FROM ubuntu:22.04

WORKDIR /image_alignment

COPY requirements.txt ./

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .
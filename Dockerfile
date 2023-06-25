FROM ubuntu:22.04

LABEL maintainer="zheming.lyu"
LABEL version="1.2"

WORKDIR /setup

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
    git wget curl net-tools \
    python3 python-is-python3 pip \
    espeak lame libsndfile1-dev \
    uvicorn \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/

ADD monotonic_align_source/monotonic_align /setup/monotonic_align
RUN cd /setup/monotonic_align && python setup.py build && python setup.py install

WORKDIR /vits
# Build container from local project
FROM python:3.7-alpine3.10

COPY . /f5-cli

WORKDIR /f5-cli

RUN apk add --no-cache --update openssh==8.1_p1-r0 python3==3.7.5-r1 python3-dev=3.7.5-r1 libffi-dev==3.2.1-r6 bash==5.0.0-r0 build-base==0.5-r1 openssl-dev==1.1.1d-r2

RUN pip install --upgrade pip==20.0.2

# Install requirements
RUN pip install -r requirements.txt

# Install f5-cli locally
RUN pip install .

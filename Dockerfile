FROM python:3.7-alpine

COPY . /f5-cli

WORKDIR /f5-cli

RUN apk add --no-cache --update openssh==7.9_p1-r6 python3==3.6.9-r2 python3-dev=3.6.9-r2 libffi-dev==3.2.1-r6 bash==4.4.19-r1 build-base==0.5-r1 openssl-dev==1.1.1d-r2
#bash curl git vim build-base python3-dev python3 libffi-dev openssl-dev 

RUN pip install --upgrade pip==20.0.2

# Install requirements
RUN pip install -r requirements.txt

# Install f5-cli locally
RUN pip install .

#Uncomment to install f5-cli from pypi
#RUN pip install f5-cli==0.9.1


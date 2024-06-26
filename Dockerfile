
# Dockerfile 04/2021
# Python environment for exporting data analysis for processing on remote systems. 


# Ubuntu version 20.04
FROM ubuntu:20.04


MAINTAINER Alex Perkins <a.j.p.perkins@sms.ed.ac.uk>

# Updates Ubuntu
RUN apt-get update && apt-get -y update && apt update


# Installs Python
RUN apt-get install -y build-essential python3.6 python3-pip python3-dev

# Upgrades the Python Package Manager
RUN pip3 -q install pip --upgrade



# Makes a directory in the Ubuntu Root called /app
# Sets it to the directory to work in
# Copies everything over from the current local directory into /app
RUN mkdir /src/
WORKDIR /src/
COPY . /src/


# Installs the Python packages
RUN pip3 install -r /src/installation/requirements.txt


EXPOSE 8052

HEALTHCHECK CMD curl --fail http://localhost:443/_stcore/health

ENTRYPOINT ["streamlit", "run", "/src/Home.py"]

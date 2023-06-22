
# Dockerfile 04/2021
# Python environment for exporting data analysis for processing on remote systems. 

FROM python:3.8.5
MAINTAINER Alex Perkins <a.j.p.perkins@sms.ed.ac.uk>
WORKDIR /app
COPY . /app
RUN python -m pip install -r requirements.txt

EXPOSE 8888

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
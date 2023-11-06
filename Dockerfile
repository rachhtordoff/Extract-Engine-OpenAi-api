FROM python:3.10
MAINTAINER Rachael Tordoff


RUN pip3 -q install gunicorn==19.9.0 eventlet==0.24.1
RUN apt-get install -y libpq-dev

# copy and install requirements before the rest of the sourcecode to allow docker caching to work
copy requirements.txt /opt/requirements.txt
copy requirements_test.txt /opt/requirements_test.txt
RUN pip3 install -q -r /opt/requirements.txt && \
    pip3 install -q -r /opt/requirements_test.txt
    

COPY / /opt/

EXPOSE 8000

WORKDIR /opt

CMD ["/usr/local/bin/gunicorn", "-k", "eventlet", "--timeout", "100000", "-w", "4", "--pythonpath", "/opt", "--access-logfile", "-", "manage:manager.app", "--reload", "-b", "0.0.0.0:8000"]

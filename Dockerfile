FROM python:3

WORKDIR /opt/iot

COPY requirements.txt /opt/iot
COPY *.py /opt/iot/

RUN pip3 install --no-cache-dir -r /opt/iot/requirements.txt
CMD [ "python3", "/opt/iot/iothub2influxdb.py" ]

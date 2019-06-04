from azure.eventhub import EventData, EventHubClient, Offset
from influx_adapter import InfluxAdapter
import logging, os, configparser, time, threading, functools
import multiprocessing.dummy

logger = logging.getLogger(__name__)
stop_event = threading.Event()


def receivefunc(receiver, influxdb):
    while not stop_event.is_set():
        received = receiver.receive(timeout=0.5)
        for r in received:
            body = r.body_as_json()
            fields = {'temperature': body['temperature'], 'humidity': body['humidity'], 'pressure': body['pressure'] }
            msg = influxdb.convert_entry(r.device_id.decode('utf-8'), body['timestamp'], fields)
            influxdb.add([msg])


def get_config(fname):
    configp = configparser.ConfigParser()
    configp.read(fname)
    iothub_config = configp['azure']
    influx_config = configp['influxdb']
    return iothub_config, influx_config


def run():
    logger.info('starting')
    iot_conf, influx_conf = get_config('conf/config.ini')
    influxdb = InfluxAdapter(influx_conf['HOSTNAME'], influx_conf['PORT'], influx_conf['USER'], influx_conf['PASSWORD'], influx_conf['DATABASE'])
    client = EventHubClient.from_iothub_connection_string(iot_conf['IOTHUB_CONNSTR'], debug=True)

    info = {'partition_count': 2, 'partition_id': ['0']}
    receivers = []
    for pid in info['partition_id']:
        receivers.append(client.add_receiver("$default", '1', offset=Offset("@latest"), operation='/messages/events'))

    try:
        client.run()
        p = multiprocessing.dummy.Pool(info['partition_count'])
        receiverfunc = functools.partial(receivefunc, influxdb=influxdb)
        p.map(receiverfunc, receivers)
    except KeyboardInterrupt:
        logger.info('stopping')
        stop_event.set()
    finally:
        client.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    run()
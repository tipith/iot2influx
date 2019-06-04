from influxdb import InfluxDBClient
import logging, os, time

logger = logging.getLogger('influx adapter')


class InfluxAdapter:

    def __init__(self, host, port, user, passw, dbname):
        self.influx = InfluxDBClient(host, port, user, passw, dbname)
        self._connect(dbname)

    def _connect(self, dbname):
        while True:
            try:
                dbs = self.influx.get_list_database()
                if dbname not in dbs:
                    self.influx.create_database(dbname)
            except Exception:
                logger.exception("Error connecting to InfluxDB. Retrying in 30sec")
                time.sleep(30)
                continue
            else:
                logging.warn("connected to influxdb")
                break

    def _write(self, payload):
        while True:
            try:
                logger.warn(payload)
                self.influx.write_points(payload)
            except Exception:
                logger.exception("Error writing to InfluxDB. Retrying in 30sec")
                time.sleep(30)
                continue
            else:
                break

    def convert_entry(self, devid, timestamp, msg):
        return {'measurement': devid, 'time': timestamp, 'fields': msg}

    def add(self, msg):
        self._write(msg)
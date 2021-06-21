from network import Bluetooth
import math
from SI7006A20 import SI7006A20
import _thread
import time

MIN_TEMP_DIFF = 1.0
MIN_HUMIDITY_DIFF = 1.0

SERVICE_ENVIRONMENT_SENSING = 0x181A
CHARACTERISTIC_HUMIDITY = 0x2A6F
CHARACTERISTIC_TEMPERATURE = 0x2A6E

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = _thread.start_new_thread(fn, args, kwargs)
        return thread
    return wrapper

class TemperatureService:
    def __init__(self, pysense, bluetooth):
        self._si = SI7006A20(pysense)
        self._service = bluetooth.service(
            uuid=SERVICE_ENVIRONMENT_SENSING,
            isprimary=True,
            nbr_chars=2)
        self._charTemperature = self._service.characteristic(
            uuid=CHARACTERISTIC_TEMPERATURE,
            properties=Bluetooth.PROP_READ | Bluetooth.PROP_NOTIFY)
        self._charHumidity = self._service.characteristic(
            uuid=CHARACTERISTIC_HUMIDITY,
            properties=Bluetooth.PROP_READ | Bluetooth.PROP_NOTIFY)
        self._run = False
        self._temperature = None
        self._humidity = None

    def _readTemperature(self):
        return self._si.temperature()

    def _writeTemperature(self, temp):
        self._charTemperature.value(str(temp))

    def _updateTemperature(self):
        currentTemperature = self._readTemperature()
        if self._temperature == None or math.fabs(self._temperature - currentTemperature) > float(MIN_TEMP_DIFF):
            self._temperature = currentTemperature
            self._writeTemperature(self._temperature)

    def _readHumidity(self):
        return self._si.humidity()

    def _writeHumidity(self, humidity):
        self._charHumidity.value(str(humidity))

    def _updateHumidity(self):
        currentHumidity = self._readHumidity()
        if self._humidity == None or math.fabs(self._humidity - currentHumidity) > float(MIN_HUMIDITY_DIFF):
            self._humidity = currentHumidity
            self._writeHumidity(self._humidity)

    @threaded
    def start(self):
        self._run = True
        self._updateTemperature()
        self._updateHumidity()
        self._service.start()
        while self._run:
            time.sleep(0.5)
            self._updateTemperature()
            self._updateHumidity()
        # self._service.stop()

    def stop(self):
        self._run = False

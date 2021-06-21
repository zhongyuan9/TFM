from network import Bluetooth
import math
import _thread
import time

SERVICE_BATTERY_SERVICE = 0x180F
CHARACTERISTIC_BATTERY_LEVEL = 0x2A19

def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = _thread.start_new_thread(fn, args, kwargs)
        return thread
    return wrapper

class BatteryService:
    def __init__(self, pysense, bluetooth):
        self._pysense = pysense
        self._service = bluetooth.service(
            uuid=SERVICE_BATTERY_SERVICE,
            isprimary=True,
            nbr_chars=1)
        self._charBatteryLevel = self._service.characteristic(
            uuid=CHARACTERISTIC_BATTERY_LEVEL,
            properties=Bluetooth.PROP_READ | Bluetooth.PROP_NOTIFY)
        self._run = False
        self._batteryLevel = None

    def _readBatteryLevel(self):
        return self._pysense.read_battery_voltage()

    def _writeBatteryLevel(self, batteryLevel):
        self._charBatteryLevel.value(str(batteryLevel))

    def _updateBatteryLevel(self):
        currentBatteryLevel = self._readBatteryLevel()
        self._writeBatteryLevel(currentBatteryLevel)

    @threaded
    def start(self):
        self._run = True
        self._updateBatteryLevel()
        self._service.start()
        while self._run:
            time.sleep(5)
            self._updateBatteryLevel()
        # self._service.stop()

    def stop(self):
        self._run = False

import time
import ujson
import pycom
from network import Bluetooth
from SI7006A20 import SI7006A20   #温度传感器 湿度传感器
from pysense import Pysense
from LIS2HH12 import LIS2HH12
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE
from LTR329ALS01 import LTR329ALS01 #光感


BLEConnected = False

py = Pysense()

def connectionCallback(e):
    events = e.events()
    global BLEConnected
    if events & Bluetooth.CLIENT_CONNECTED:
        BLEConnected = True
        print("LJCG")
    elif events & Bluetooth.CLIENT_DISCONNECTED:
        BLEConnected = False
        print("DKLJ")


def char1_cb_handler(chr, data):
    events, value = data
    if events & Bluetooth.CHAR_WRITE_EVENT:
        print("GBRGB")
        pycom.rgbled(int.from_bytes(bytearray(value), 'big'))
    elif events & Bluetooth.CHAR_READ_EVENT:
        print("Read Request")





mp = MPL3115A2(py,mode=ALTITUDE)
wendu = str(mp.temperature())



pycom.heartbeat(False)

Bluetooth().set_advertisement(name='LoPy', service_uuid=12345)
# Callback event for on connected and on disconnected
# Llamada de retorno sobre los eventos connectado y desconectado

# Triggers Bluetooth.NEW_ADV_EVENT, Bluetooth.CLIENT_CONNECTED, or Bluetooth.CLIENT_DISCONNECTED
Bluetooth().callback(trigger=Bluetooth.CLIENT_CONNECTED |
                     Bluetooth.CLIENT_DISCONNECTED, handler=connectionCallback)

# Start sending BLE advertisements.
# Inicia los mensajes de anuncio de BLE
Bluetooth().advertise(True)



# Create and init BLE service and declare 2 characteristics
srv = Bluetooth().service(uuid=12345, isprimary=True, nbr_chars=2, start=True)


# Characteristics Bluetooth.PROP_NOTIFY,
# Info https://www.oreilly.com/library/view/getting-started-with/9781491900550/ch04.html
char1 = srv.characteristic(uuid=54321, properties=Bluetooth.PROP_NOTIFY, value=ujson.dumps({}))


char2 = srv.characteristic(uuid=64321, value=0xff00)

char1_cb = char2.callback(
    trigger=Bluetooth.CHAR_WRITE_EVENT, handler=char1_cb_handler)


while True:
    time.sleep(10)
    json = ujson.dumps({"h": wendu})
    print("json  =  " + json)
    #wd = wendu
    if BLEConnected:
        char1.value(json)

# Germán Andrés Xander 2023

from machine import Pin, Timer, unique_id
import dht
import time
import json
import ubinascii
from collections import OrderedDict
from settings import SERVIDOR_MQTT
from umqtt.robust import MQTTClient

CLIENT_ID = ubinascii.hexlify(unique_id()).decode('utf-8')
print(CLIENT_ID)

mqtt = MQTTClient(CLIENT_ID, SERVIDOR_MQTT,
                  port=8883, keepalive=40, ssl=True)

sw = Pin(27, Pin.OUT)
led = Pin(2, Pin.OUT)

led.value(1)
time.sleep(.2)
led.value(0)
time.sleep(.2)
led.value(1)
time.sleep(.2)
led.value(0)

def sub_cb(topic, msg):
    print((topic, msg))
    if msg==b"apagar":
        led.value(0)
        sw.value(0)
    if msg==b"encender":
        led.value(1)
        sw.value(1)
    mqtt.publish(f"iot/{CLIENT_ID}/estado",str(sw.value()))

mqtt.set_callback(sub_cb)
mqtt.connect()
mqtt.subscribe(f"iot/{CLIENT_ID}/comando")

def transmitir(pin):
    mqtt.publish(f"iot/{CLIENT_ID}/estado",str(sw.value()))

timer1 = Timer(1)
timer1.init(period=30000, mode=Timer.PERIODIC, callback=transmitir)

while 1:
    mqtt.wait_msg()

mqtt.disconnect()
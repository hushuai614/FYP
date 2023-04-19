from machine import Pin
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
esp.osdebug(None)
import gc
gc.collect()

led = Pin(22, Pin.OUT) 

ssid = 'Linksys17282'
password = 'WQL13244'
mqtt_server = '192.168.1.114' #Replace with your MQTT Broker IP

client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'esp32/led'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

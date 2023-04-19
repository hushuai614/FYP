# MQ-2 library to use gas sensor with Raspberry PI Pico (MicroPython)

from mq2 import MQ2
import utime
import network
import utime
from umqttsimple import MQTTClient
import ubinascii
import time

pin=26

ssid = 'Linksys17282'
password = 'WQL13244'
mqtt_server = '192.168.1.114'
#EXAMPLE IP ADDRESS or DOMAIN NAME
#mqtt_server = '192.168.1.106'

client_id = ubinascii.hexlify(machine.unique_id())

topic_pub_Smoke = b'esp/dht/Smoke'
topic_pub_LPG = b'esp/dht/LPG'
topic_pub_Methane = b'esp/dht/Methane'
topic_pub_Hydrogen = b'esp/dht/Hydrogen'


last_message = 0
message_interval = 5

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')

def connect_mqtt():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server)
  #client = MQTTClient(client_id, mqtt_server, user=your_username, password=your_password)
  client.connect()
  print('Connected to %s MQTT broker' % (mqtt_server))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()
try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

sensor = MQ2(pinData = pin, baseVoltage = 3.3)

print("Calibrating")
sensor.calibrate()
print("Calibration completed")
print("Base resistance:{0}".format(sensor._ro))

def check_Smoke():
    print('Check Smoke Starting...')
    while True:
        try:
            Smoke=(b'{:.1f},'.format(sensor.readSmoke()))
            return Smoke
            time.sleep(5)
        except:
            pass
        
def check_LPG():
    print('Check LPG Starting...')
    while True:
        try:
            LPG=(b'{:.1f},'.format(sensor.readLPG()))
            return LPG
            time.sleep(5)
        except:
            pass
        
def check_Methane():
    print('Check Methane Starting...')
    while True:
        try:
            Methane=(b'{:.1f},'.format(sensor.readMethane()))
            return Methane
            time.sleep(5)
        except:
            pass
        
def check_Hydrogen():
    print('Check Hydrogen Starting...')
    while True:
        try:
            Hydrogen=(b'{:.1f},'.format(sensor.readHydrogen()))
            return Hydrogen
            time.sleep(5)
        except:
            pass
while True:
  try:
    if (time.time() - last_message) > message_interval:
      Smoke = check_Smoke()
      print("Smoke: {:.1f}".format(sensor.readSmoke())+" - ", end="")
      LPG = check_LPG()
      print("LPG: {:.1f}".format(sensor.readLPG())+" - ", end="")
      Methane=check_Methane()
      print("Methane: {:.1f}".format(sensor.readMethane())+" - ", end="")
      Hydrogen=check_Hydrogen()
      print("Hydrogen: {:.1f}".format(sensor.readHydrogen()))
      client.publish(topic_pub_Smoke, Smoke)
      client.publish(topic_pub_LPG, LPG)
      client.publish(topic_pub_Methane, Methane)
      client.publish(topic_pub_Hydrogen, Hydrogen)
      last_message = time.time()
  except OSError as e:
    restart_and_reconnect()


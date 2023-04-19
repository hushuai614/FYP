from machine import Pin, SoftI2C
from machine import Pin, ADC
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import esp
import network
import time
esp.osdebug(None)
import gc
gc.collect()

ssid = 'Linksys17282'
password = 'WQL13244'
mqtt_server = '192.168.1.114'
#EXAMPLE IP ADDRESS or DOMAIN NAME
#mqtt_server = '192.168.1.106'

client_id = ubinascii.hexlify(machine.unique_id())

topic_pub_moisture = b'esp/dht/moisture'
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


# Soil Moisture
soil = ADC(Pin(35))
m = 100

min_moisture=0
max_moisture=4095

soil.atten(ADC.ATTN_11DB)       #Full range: 3.3v
soil.width(ADC.WIDTH_12BIT)     #range 0 to 4095

def check_moisture():
    print('Check Moisture Starting...')
    global m
    while True:
        try:
            soil.read()
            time.sleep(2)
            m = (max_moisture-soil.read())*100/(max_moisture-min_moisture)
            moisture = (b'{0:3.1f},'.format(m))
            return moisture
            time.sleep(5)
        except:
            pass

# START
print('Starting...')

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    if (time.time() - last_message) > message_interval:
      moisture = check_moisture()
      print(moisture)
      client.publish(topic_pub_moisture, moisture)
      last_message = time.time()
  except OSError as e:
    restart_and_reconnect()

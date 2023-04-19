# Complete project details at https://RandomNerdTutorials.com
import ssd1306
rst = machine.Pin(16, machine.Pin.OUT)
rst.value(1)
i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4), freq=400000)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
temp=b'NA'
hum=b'NA'
def sub_cb(topic, msg):
  if topic==b'esp/dht/temperature':
      global temp
      temp=msg[-5:-1]
      print(temp)
      return(temp)
  if topic==b'esp/dht/humidity':
      global hum
      hum=msg[-5:-1]
      print(hum)
      return(hum)


 


def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub_temp,topic_sub_hum
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub_temp)
  client.subscribe(topic_sub_hum)
  
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub_temp))
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub_hum))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

while True:
  try:
    new_message = client.check_msg()
    time.sleep(1)
    oled.fill(0)
    oled.text('HUSHUAI MQTT', 10, 0)
    # Display the temperature
    oled.text('Temperature *C:', 10, 20)
    oled.text(temp[0:], 90, 30)
    # Display the humidity
    oled.text('Humidity %:', 10, 40)
    oled.text(hum[0:], 90, 50)

    # Update the screen display
    oled.show()
  except OSError as e:
    restart_and_reconnect()

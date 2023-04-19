def sub_cb(topic, msg):
  print ('Received Message %s from topic %s' %(msg, topic))
  if msg == b'false':
    led.value(0)
    print('LED is now OFF')
  elif msg == b'true':
    led.value(1)
    print('LED is now ON')

def connect_and_subscribe():
  global client_id, mqtt_server, topic_sub
  client = MQTTClient(client_id, mqtt_server)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
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
       new_msg = client.check_msg()
     
  except OSError as e:
    restart_and_reconnect

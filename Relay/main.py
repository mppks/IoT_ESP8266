from machine import Pin
from umqtt.simple import MQTTClient
import config

relay = Pin(0, Pin.OUT)
relay.value(1)


def sub_callback(topic, msg):
    if msg == b'On':
        relay.value(0)
        print("on")
    else:
        relay.value(1)
        print("off")
    

mqtt = MQTTClient(client_id=config.MQTT_CLIENT_ID, server=config.MQTT_SERVER,
                  user=config.MQTT_USER, password=config.MQTT_PASSWORD)
mqtt.set_callback(sub_callback)
mqtt.connect()
mqtt.subscribe(config.MQTT_TOPIC)

try:
    while True:
        mqtt.wait_msg()
except Exception as e:
    if e.args[0] == -1:
        print('Socket disconnected')
    else:
        print(e)
finally:
    mqtt.disconnect()

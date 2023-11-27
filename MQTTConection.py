import paho.mqtt.client as mqtt

MQTT_BROKER = "46.17.108.113"
MQTT_PORT = 1883
MQTT_TOPIC_OXIMETRO = "/TEF/Hosp108/attrs/o"
MQTT_TOPIC_HEARTBEATS = "/TEF/Hosp108/attrs/h"
MQTT_TOPIC_TEMPERATURE = "/TEF/Hosp108/attrs/t"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(MQTT_TOPIC_OXIMETRO)
    client.subscribe(MQTT_TOPIC_HEARTBEATS)
    client.subscribe(MQTT_TOPIC_TEMPERATURE)

def on_message(client, userdata, msg):
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_forever()

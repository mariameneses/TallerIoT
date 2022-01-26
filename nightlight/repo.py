import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
import json
import paho.mqtt.client as mqtt

# print('Hello World!')

CounterFitConnection.init('127.0.0.1', 5001)

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

# while True:
#     light = light_sensor.light
#     print('Light level:', light)

#     if light < 300:
#         led.on()
#     else:
#         led.off()

#     time.sleep(3)

id = '3233cc76-9b52-42ce-9236-98fa9fb11f9c'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'nightlight_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['led_on']:
        led.on()
    else:
        led.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
    light = light_sensor.light
    print('Light level:', light)

    mqtt_client.publish(client_telemetry_topic, json.dumps({'light' : light}))
    time.sleep(5)

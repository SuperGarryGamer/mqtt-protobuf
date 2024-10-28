import paho.mqtt.client as mqtt
import numpy as np
import config as cfg
import weather_pb2
import time


def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(cfg.BROKER_IP, 1883, 60)
    main_loop(mqtt_client)

def main_loop(client: mqtt.Client):
    client.loop_start()
    for i in range(10):
        client.publish(topic="temp", payload=fake_weather())
        time.sleep(0.5)
    client.loop_stop()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to {cfg.BROKER_IP}, code {str(rc)}")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {str(msg.payload)}")

def fake_weather():
    weather = weather_pb2.Weather()
    weather.timestamp = int(time.time())
    weather.temp_centicelsius = int(np.random.normal(2000, 500))
    weather.pres_hpa = int(np.random.normal(1013, 5))
    weather.descriptor = np.random.randint(0, 7)
    return weather.SerializeToString()


if __name__ == "__main__":
    main()
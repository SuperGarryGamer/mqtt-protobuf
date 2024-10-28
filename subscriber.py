import paho.mqtt.client as mqtt
import config as cfg
import weather_pb2
import datetime

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(cfg.BROKER_IP, 1883, 60)
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to {cfg.BROKER_IP}, code {str(rc)}")

def on_message(client, userdata, msg):
    if msg.topic == "temp":
        pretty_print_protobuf(msg.content)

def pretty_print_protobuf(raw: str):
    weather = weather_pb2.Weather()
    weather.ParseFromString(raw)
    print(datetime.date.fromtimestamp(weather.timestamp).ctime())
    print(f"Temperature: {weather.temp_centicelsius / 100}C")
    print(f"Pressure: {weather.pres_hpa}hPa")
    print(f"Conditions: {weather.desciptor}")

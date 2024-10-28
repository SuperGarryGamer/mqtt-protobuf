import paho.mqtt.client as mqtt
import config as cfg
import weather_pb2
import datetime

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(cfg.BROKER_IP, 1883, 60)
    mqtt_client.subscribe("weather")
    mqtt_client.loop_forever()

def on_connect(client, userdata, flags, rc):
    print(f"Connected to {cfg.BROKER_IP}, code {str(rc)}")

def on_message(client, userdata, msg):
    print(f"receiving new {msg.topic} :3")
    pretty_print_protobuf(msg.payload)

def pretty_print_protobuf(raw: str):
    weather = weather_pb2.Weather()
    weather.ParseFromString(raw)
    print(datetime.datetime.fromtimestamp(weather.timestamp).ctime())
    print(f"Temperature: {weather.temp_centicelsius / 100}C")
    print(f"Pressure: {weather.pres_hpa}hPa")
    print(f"Conditions: {weather_pb2.Weather.Descriptor.Name(weather.descriptor)}")
    print("")

if __name__ == "__main__":
    main()
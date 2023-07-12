import machine
import time
import dht
from umqtt.simple import MQTTClient
import network

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
print(" Connected!")

# Configuración de los parámetros MQTT
mqtt_server = "bf2200fe67bf4e11aac299e657c2991f.s2.eu.hivemq.cloud"
mqtt_topic = "domotica/temperatura_humedad"
mqtt_client_id = "pedrorpa"

# Configuración del sensor de temperatura y humedad
dht_pin = machine.Pin(0)
dht_sensor = dht.DHT11(dht_pin)

# Conexión MQTT
client = MQTTClient(mqtt_client_id, mqtt_server)

# Función de callback para procesar los mensajes MQTT recibidos
def mqtt_callback(topic, msg):
    print("Mensaje recibido en el topic: {}".format(topic))
    print("Contenido del mensaje: {}".format(msg))

# Conexión al broker MQTT
client.set_callback(mqtt_callback)
client.connect()

# Nos suscribimos al topic
client.subscribe(mqtt_topic)

# Publicamos un mensaje al broker
mensaje = "Hola, este es un mensaje de prueba"
client.publish(mqtt_topic, mensaje.encode())

# Bucle principal
while True:
    try:
        # Envía los datos de temperatura y humedad a través de MQTT
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        message = "Temperatura: {}°C, Humedad: {}%".format(temperature, humidity)
        client.publish(mqtt_topic, message.encode())

        # Verifica si hay mensajes MQTT recibidos
        client.check_msg()

        time.sleep(1)
    except OSError as e:
        print("Error de conexión MQTT:", e)

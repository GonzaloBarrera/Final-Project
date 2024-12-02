from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from allModules import read_temperature, read_soil_moisture, read_light_intensity
import config
import json
import time

#set time
date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
print (f"Timestamp:{date}")

# user specified callback function
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# configure the MQTT client
myMQTTClient = AWSIoTMQTTClient(config.CLIENT_ID)
myMQTTClient.configureEndpoint(config.AWS_HOST, config.AWS_PORT)
myMQTTClient.configureCredentials(config.AWS_ROOT_CA, config.AWS_PRIVATE_KEY, config.AWS_CLIENT_CERT)
myMQTTClient.configureConnectDisconnectTimeout(config.CONN_DISCONN_TIMEOUT)
myMQTTClient.configureMQTTOperationTimeout(config.MQTT_OPER_TIMEOUT)
 
#Connect to MQTT Host
if myMQTTClient.connect():
    print('AWS connection succeeded')

# Subscribe to topic
myMQTTClient.subscribe(config.TOPIC, 1, customCallback)
time.sleep(2)

# Send message to host
loopCount = 0
while loopCount < 10:
    temperature = read_temperature()
    adc_value, moisture = read_soil_moisture()
    light_intensity = read_light_intensity()
    payload=json.dumps({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "moisture": moisture,
        "light_intensity": light_intensity
    }); 
    
    print(f"Publishing payload: {payload}")
    
    myMQTTClient.publish(config.TOPIC, payload, 1)
    loopCount += 1
    time.sleep(2)

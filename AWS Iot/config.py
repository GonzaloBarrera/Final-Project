# AWS general configuration
AWS_PORT = 8883
AWS_HOST = 'acio74frd7t67-ats.iot.us-east-1.amazonaws.com'
AWS_ROOT_CA = '/home/gonzalo/certs/aws_root.pem'
AWS_CLIENT_CERT = '/home/gonzalo/certs/aws_client.crt'
AWS_PRIVATE_KEY = '/home/gonzalo/certs/aws_private.key'
################## Subscribe / Publish client #################
CLIENT_ID = 'fromPi'
TOPIC = 'gonzalo/device/raspberry/data'
#TOPIC = 'champlain/republish'
OFFLINE_QUEUE_SIZE = -1
DRAINING_FREQ = 2
CONN_DISCONN_TIMEOUT = 10
MQTT_OPER_TIMEOUT = 5

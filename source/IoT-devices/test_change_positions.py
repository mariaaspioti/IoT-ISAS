import random
import json
import paho.mqtt.client as mqtt
import requests

# MQTT broker details
broker = '150.140.186.118'
port = 1883
client_id = "KA_ISAS"
topic = "ISAS/test"


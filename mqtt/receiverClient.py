#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import traceback
import configparser
import datetime
import json
import sys
import logging
sys.path.append("..")


cf = configparser.ConfigParser()
cf.read("../web.conf")
password = cf.get("mqttServer", "password")
username = cf.get("mqttServer", "username")
hostname = cf.get("mqttServer", "hostname")
port = cf.getint("mqttServer", "port")
qos = cf.getint("mqttServer", "rdqos")
print(password,username,hostname,port,qos)
def log(strs):
    print(strs)
    logging.info("time:%s "% datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +str(strs))


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    log("connect to mqtt server return code: "+str(rc))
    topics = []
    topic = "stagebo/chatroom"
    topics.append((topic,qos))

    client.subscribe(topics)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #在这里处理业务逻辑
    topic = msg.topic
    tpInfo = topic.split("/")  # tdqs/00005/1.0.0/rd/4
    ms = str(msg.payload, "utf-8")
    print(ms)
if __name__ == "__main__":
    print("start")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username,password)
    client.connect(hostname, port)

    client.loop_forever()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import random
import json
import time
import traceback

import sys
sys.path.append("..")
import logging
import datetime
import configparser

cf = configparser.ConfigParser()
cf.read("../web.conf")
password = cf.get("mqttServer", "password")
username = cf.get("mqttServer", "username")
hostname = cf.get("mqttServer", "hostname")
port = cf.getint("mqttServer", "port")
qos = cf.getint("mqttServer", "rdqos")



def log(strs):
    logging.info("time:%s "% datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +str(strs))

idx = 0
def sendMsg():
    msgs = []
    global idx
    nowStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    topic = "stagebo/chatroom"


    msg = {
        "time": nowStr,
        "data": "this is data."
    }


    msgItem = {'topic': topic, 'payload': msg, 'qos': qos}
    # msgItem = (topic,msg)
    msgs.append(msgItem)
    print(idx)
    publish.multiple(msgs,
                     auth={
                         'username': username,
                         'password': password
                     },
                     port=port,
                     protocol=mqtt.MQTTv311,
                     hostname=hostname)


    idx += 1
    # time.sleep(1)


if __name__ == "__main__":
    while True:
        try:
            sendMsg()
        except:
            traceback.print_exc()

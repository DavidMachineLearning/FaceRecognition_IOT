#!/usr/bin python3
# -*- coding: utf-8 -*-

__author__ = "David Forino AI Solutions"
__license__ = "MIT"
__version__ = "1.0.0"

import os
import cv2
import uuid
import argparse
import numpy as np
from time import time
from datetime import datetime
import paho.mqtt.client as mqtt


# arguments
parser = argparse.ArgumentParser(description="MQTTViewStream, program created by David Forino AI Solutions "
                                             "(https://davidforino-aisolutions.com). Visualize and save images stream "
                                             "via MQTT!")
parser.add_argument("--broker_ip", help="IP address of your MQTT broker", type=str)
parser.add_argument("--topic", help="On which topic to stream the video", type=str, default="live_streaming")
parser.add_argument("--timeout", help="Timeout to close the live view window but keeps the connection",
                    type=int, default=15)
parser.add_argument("--save_dir", help="Directory where to store the images, if this argument is given, it "
                                       "won't show any image", type=str, default="")

args = parser.parse_args()


def on_connect(_, __, ___, rc):
    global client
    print(f"Connected with result code {rc}")
    client.subscribe(args.topic)


def on_disconnect(_, __, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    else:
        print("Disconnected.")
    cv2.destroyAllWindows()


def on_message_show(_, __, msg):
    global timer
    timer = time()
    image = cv2.imdecode(np.asarray(bytearray(msg.payload), dtype=np.uint8), cv2.IMREAD_COLOR)
    cv2.imshow(msg.topic, image)
    cv2.waitKey(1)


def on_message_save(_, __, msg):
    global save_dir
    with open(f"{save_dir}/{str(uuid.uuid4())}.jpg", "wb") as file:
        file.write(msg.payload)


# setup the client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message_save if args.save_dir else on_message_show
client.on_disconnect = on_disconnect
client.connect(args.broker_ip, 1883)

# save images
if args.save_dir:
    today = datetime.today().strftime("%d_%m_%Y")
    save_dir = f"{args.save_dir}/{today}"
    os.makedirs(save_dir, exist_ok=True)
    client.loop_forever()

# show live video
else:
    timer = 0
    try:
        while True:
            # stop displaying
            if timer and (time() - timer) > args.timeout:
                print("Closing windows...")
                cv2.destroyAllWindows()
                timer = 0

            client.loop(0.1)

    except KeyboardInterrupt:
        print('Program interrupted...')

    finally:
        client.disconnect()

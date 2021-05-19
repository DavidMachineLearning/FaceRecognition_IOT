#!/usr/bin python3
# -*- coding: utf-8 -*-

__author__ = "David Forino AI Solutions"
__license__ = "MIT"
__version__ = "1.0.0"

import os
import cv2
import argparse
from time import time, sleep
import paho.mqtt.publish as publish


def size(s):
    """Handling argument errors"""
    try:
        width, height = map(int, s.split(','))
        return width, height
    except:
        raise argparse.ArgumentTypeError("Size must be <width,height> in pixel values")


def face_detection(cascade, img, scale_factor=1.1):
    """
    Apply face detection to the give image. If 1 face is detected, the image is cropped around the face + a delta.
    If there is no face returns None, if there are multiple faces returns the biggest one.
    :param cascade: The cascade classifier used for the detection
    :param img: The image to be used
    :param scale_factor: Parameter specifying how much the image size is reduced at each image scale
    :return: cropped image or None
    """
    height, width = img.shape[:2]

    # gray scale image is necessary for the classifier to work
    gray = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(gray, scaleFactor=scale_factor, minNeighbors=5)

    if len(faces) >= 1:
        # get biggest face
        sizes = [w * h for (x, y, w, h) in faces]
        (x, y, w, h) = faces[max(enumerate(sizes), key=lambda x: x[1])[0]]

        # increase dimensions to compensate error
        x = max(0, x - int(w * 0.1))
        y = max(0, y - int(h * 0.35))
        w = min(width, int(w * 1.1))
        h = min(height, int(h * 1.55))
        return img[y:y+h, x:x+w, :]

    else:
        return None


def pause(start, fps):
    """
    Pause the program to remain at the specified maximum FPS rate.
    :param start: Start time of the loop
    :param fps: maximum fps allowed
    """
    stop = time()
    sleep_time = max(0, 1 / fps - (stop - start))
    sleep(sleep_time)


# arguments
parser = argparse.ArgumentParser(description="MQTTVideoStream, program created by David Forino AI Solutions "
                                             "(https://davidforino-aisolutions.com). Stream video from your "
                                             "camera via MQTT!")
parser.add_argument("--broker_ip", help="IP address of your MQTT broker", type=str)
parser.add_argument("--topic", help="On which topic to stream the video", type=str, default="live_streaming")
parser.add_argument("--max_fps", help="Maximum FPS desired value", type=int, default=5)
parser.add_argument("-f", "--face_detection", help="Apply face detection and send only the image cropped to the face."
                                                   " If no face is detected, sends nothing."
                                                   " If multiple faces are detected, sends the biggest one only.",
                    action="store_true")
parser.add_argument("--resize", help="Resize image to <width,height>", type=size, default=(128, 128))

args = parser.parse_args()
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_clf = cv2.CascadeClassifier(os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml'))

# define a video capture object
camera = cv2.VideoCapture(0)

print(f"Streaming at {args.max_fps} FPS started...")
# infinite loop
while True:
    start_time = time()
    # Capture 1 frame
    _, original_frame = camera.read()

    # apply face detection
    if args.face_detection:
        original_frame = face_detection(haar_clf, original_frame, scale_factor=1.1)

        if original_frame is None:
            print("Face not detected...")
            pause(start_time, args.max_fps)
            continue

    # resize frame and convert it to string
    original_frame = cv2.resize(original_frame, args.resize, interpolation=cv2.INTER_AREA)
    byte_img = cv2.imencode(".jpg", original_frame)[1].tobytes()

    # send image via mqtt
    publish.single(args.topic, byte_img, hostname=args.broker_ip)
    pause(start_time, args.max_fps)

# FaceRecognition_IOT
Face recognition using Deep Learning running on a Jetson Nano, which receives streaming video data from a Raspberry Pi via MQTT.

### Setup
- 1 Raspberry PI (better a 4 or 3B+) will be the MQTT Broker, there you need to install Raspberrypi OS and run on a terminal "sudo apt-get install -y mosquitto mosquitto-clients".

- On the Raspberry PI (or even more than 1) which will stream the data, install the Raspberrypi OS Lite version and run on a terminal "sudo bash setup.sh".

- Setup the Jetson Nano by following the instructions provided [here](https://github.com/DavidMachineLearning/smart-home-AI).

- If you want to see the data while it is streamed, you can either use your PC and run "pip3 install paho-mqtt opencv-contrib-python" or do the same on the Raspberry PI used as a MQTT Broker.

NOTE: the code used for training and inference on the Jetson Nano will be uploaded soon...

### Usage

#### VideoStream.py
usage: VideoStream.py [-h] [--broker_ip BROKER_IP] [--topic TOPIC]
                      [--max_fps MAX_FPS] [-f] [--resize RESIZE]

MQTTVideoStream, program created by David Forino AI Solutions
(https://davidforino-aisolutions.com). Stream video from your camera via MQTT!

optional arguments:
- -h, --help             show this help message and exit
- --broker_ip BROKER_IP  IP address of your MQTT broker
- --topic TOPIC          On which topic to stream the video
- --max_fps MAX_FPS      Maximum FPS desired value
- -f, --face_detection   Apply face detection and send only the image cropped to the face. If no face is detected, sends nothing. If multiple faces are detected, sends the biggest one only.
- --resize RESIZE       Resize image to <width,height>

#### ViewStream.py
usage: ViewStream.py [-h] [--broker_ip BROKER_IP] [--topic TOPIC]
                     [--timeout TIMEOUT] [--save_dir SAVE_DIR]

MQTTViewStream, program created by David Forino AI Solutions
(https://davidforino-aisolutions.com). Visualize and save images stream via
MQTT!

optional arguments:
- -h, --help             show this help message and exit
- --broker_ip BROKER_IP  IP address of your MQTT broker
- --topic TOPIC          On which topic to stream the video
- --timeout TIMEOUT      Timeout to close the live view window but keeps the connection
- --save_dir SAVE_DIR    Directory where to store the images, if this argument is given, it won't show any image


#!/bin/sh
sudo apt-get update
sudo apt-get -y install build-essential cmake pkg-config
sudo apt-get -y install libjpeg-dev libpng-dev libtiff5-dev libjasper-dev
sudo apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get -y install libxvidcore-dev libx264-dev
sudo apt-get -y install libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libango1.0-dev
sudo apt-get -y install libatlas-base-dev gfortran
sudo apt-get -y install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get -y install libssl-dev
sudo apt-get -y install python3-dev
sudo apt-get -y install python3-pip
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=4096/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
sudo pip3 install paho-mqtt==1.5.1
sudo pip3 install numpy==1.19.5
sudo pip3 install opencv-contrib-python-headless==4.5.1.48
sudo sed -i 's/CONF_SWAPSIZE=4096/CONF_SWAPSIZE=100/g' /etc/dphys-swapfile
sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
echo "\nSETUP COMPLETE... REBOOTING NOW..."
sudo reboot

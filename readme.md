## Hardware

* Waveshare 13504 (800x480 display) with Raspberry Pi HAT
* Raspberry Pi (any version)

## Raspberry Pi setup

According to https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi

`sudo raspi-config`
Choose Interfacing Options -> SPI -> Yes Enable SPI interface
sudo reboot
Check /boot/config.txt, and you can see 'dtparam=spi=on' was written in.


Install software
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
```

## Workflow

Generate bmp file with drawer.py 

Refresh e-paper screen with app.py
import datetime
import logging
from pathlib import Path
import signal
from time import sleep
import argparse
import sys

from PIL import Image

from drawer import Drawer

logging.basicConfig(level=logging.DEBUG)

try:
    from waveshare_vendor.epd7in5_V2 import EPD
except:
    logging.critical("no waveshare_vendor lib")

run = True


def handler_stop_signals(signum, frame):
    logging.info("TERMINATE!")
    global run
    run = False


signal.signal(signal.SIGINT, handler_stop_signals)
signal.signal(signal.SIGTERM, handler_stop_signals)


def send_image(file_path, reset=False):
    epd = EPD()
    logging.info("init")
    epd.init()
    logging.info("upload image")
    Himage = Image.open(file_path)
    epd.display(epd.getbuffer(Himage))
    logging.info("Goto Sleep")
    if reset:
        epd.reset()
    else:
        epd.sleep()


def main(file_name, reset=False):
    path_img = Path(__file__).parent / file_name

    try:
        send_image(path_img, reset)
    except IOError as e:
        logging.info(e)
    except Exception as e:
        logging.info(e)
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="E-PAPER DISPLAY")
    parser.add_argument("-s", "--single", action="store_true", default=True, help="Executes single draw and exits.")
    args = parser.parse_args()
    file_name = "test.bmp"
    if args.single:
        logging.info("Exec single mode")
        Drawer(file_name=file_name).draw()
        main(file_name)
        logging.info("Exit single mode")
        sys.exit(0)

    minute_old = -1
    while run:
        minute = datetime.datetime.now().minute
        logging.info(datetime.datetime.now())
        logging.info(f"{minute=}")
        logging.info(f"{minute_old=}")
        if minute != minute_old:
            logging.info("draw")
            minute_old = minute
            Drawer(file_name=file_name).draw()
            main(file_name, reset=True)
        sleep(1)

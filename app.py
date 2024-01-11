import datetime
import logging
from pathlib import Path
import signal
from time import sleep

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


def send_image(file_path):
    epd = EPD()
    logging.info("init")
    epd.init()
    logging.info("upload image")
    Himage = Image.open(file_path)
    epd.display(epd.getbuffer(Himage))
    logging.info("Goto Sleep")
    epd.sleep()


def main(file_name):
    path_img = Path(__file__).parent / file_name

    try:
        send_image(path_img)
    except IOError as e:
        logging.info(e)
    except Exception as e:
        logging.info(e)
        pass


if __name__ == "__main__":
    file_name = "test.bmp"
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
            main(file_name)
        sleep(1)

import logging
from pathlib import Path

from PIL import Image

from waveshare_vendor.epd7in5_V2 import EPD

logging.basicConfig(level=logging.DEBUG)


def main(file_name):
    path_img = Path(__file__).parent / file_name

    try:
        epd = EPD()

        logging.info("init")
        epd.init()

        logging.info("upload image")
        Himage = Image.open(path_img)
        epd.display(epd.getbuffer(Himage))

        logging.info("Goto Sleep")
        epd.sleep()

    except IOError as e:
        logging.info(e)


if __name__ == "__main__":
    file_name = "test.bmp"
    main(file_name)

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from utils import get_buses, get_weather, get_weather_forecast

WIDTH = 800
HEIGHT = 480

FONT_BIG = ImageFont.truetype("Font.ttc", 50)
FONT_MID = ImageFont.truetype("Font.ttc", 30)
FONT_SML = ImageFont.truetype("Font.ttc", 20)

WEEKDAYS = {
    0: "Poniedziałek",
    1: "Wtorek",
    2: "Środa",
    3: "Czwartek",
    4: "Piątek",
    5: "Sobota",
    6: "Niedziela",
}


class Drawer:
    def __init__(self, file_name="test.bmp"):
        self.image = Image.new("1", (WIDTH, HEIGHT), 255)  # 255: clear the frame
        self.file_name = file_name

    def draw(self):
        self.draw_time(10, 10)
        weather = get_weather()
        self.draw_suntime(10, 150, weather)
        self.draw_weather(400, 10, weather)
        self.draw_buses(400, 300)
        self.image.save(self.file_name)

    def draw_time(self, ref_x, ref_y):
        draw = ImageDraw.Draw(self.image)
        time = datetime.now()
        minute_str = str(time.minute)
        if len(minute_str) == 1:
            minute_str = "0" + minute_str
        time_str = f"{time.hour}:{minute_str}"
        month_str = str(time.month)
        if len(month_str) == 1:
            month_str = "0" + month_str
        date_str = f"{time.day}.{month_str}.{time.year}"
        draw.text((ref_x + 5, ref_y), time_str, font=FONT_BIG)
        draw.text((ref_x, ref_y + 50), date_str, font=FONT_MID)
        draw.text((ref_x, ref_y + 80), WEEKDAYS[time.weekday()], font=FONT_MID)

    def draw_suntime(self, ref_x, ref_y, weather):
        draw = ImageDraw.Draw(self.image)
        text = f"Wsch: {weather['sunrise']}\n Zach: {weather['sunset']}"
        draw.text((ref_x, ref_y), text, font=FONT_SML)

    def draw_weather(self, ref_x, ref_y, weather):
        draw = ImageDraw.Draw(self.image)
        temp = weather["temp"]
        temp_str = f"{temp}°"
        draw.text((ref_x, ref_y), temp_str, font=FONT_BIG)
        draw.text((ref_x, ref_y + 40), weather["dscr"], font=FONT_MID)
        forecast = get_weather_forecast()
        date_now = datetime.now()
        ref = 80
        for wday in forecast:
            if wday == date_now.weekday():
                continue
            text = f"{WEEKDAYS[wday]}: {forecast[wday]['temp_min']}° - {forecast[wday]['temp_max']}°"
            draw.text((ref_x, ref_y + ref), text, font=FONT_SML)
            ref += 25

    def draw_buses(self, ref_x, ref_y):
        get_buses()


if __name__ == "__main__":
    Drawer().draw()

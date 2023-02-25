#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import requests

api_key = 'c9b9e912cc63ff0691078022b6effd59'
MY_LAT = 45.5019
MY_LNG = -73.5674
temp = ''
parameters = {
     'lat': MY_LAT,
     'lon': MY_LNG,
     'units': 'metric',
     'appid': api_key,
     'exclude': 'current,minutely,daily'
     }

my_date = time.strftime('%A')
my_month = time.strftime('%b %-d')


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
#        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default=my_date)

    def get_time(self):
        my_date = time.strftime('%A')
        my_month = time.strftime('%b %-d')
        my_time = time.strftime('%H:%M:%S')
        return my_date, my_month, my_time

    def get_temp(self):
        global temp
        response = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=parameters)
        response.raise_for_status()
        weather_data = response.json()

        temp = round(weather_data['list'][0]['main']['feels_like'], 1)
        weather_id = weather_data['list'][0]['weather'][0]['id']
        return '%d C' %(temp)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font1.LoadFont("../../../fonts/7x13.bdf")
        font2 = graphics.Font()
        font2.LoadFont("../../../fonts/6x12.bdf")
        font3 = graphics.Font()
        font3.LoadFont("../../../fonts/7x13B.bdf")

        orange = graphics.Color(255, 128, 0)
        blue = graphics.Color(0, 127, 255)
        green = graphics.Color(0, 255, 128)
        pos = offscreen_canvas.width/4
#        my_text = self.args.text

        one_hour_timer = 0
        temp = self.get_temp()

        while True:
            offscreen_canvas.Clear()
            graphics.DrawText(offscreen_canvas, font1, 5, 10, orange, self.get_time()[0])
            graphics.DrawText(offscreen_canvas, font1, pos, 23, blue, self.get_time()[1])
            graphics.DrawText(offscreen_canvas, font3, 5, 40, green, self.get_time()[2])
            graphics.DrawText(offscreen_canvas, font2, 20, 60 , blue, temp)
            time.sleep(1)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            one_hour_timer += 1
            if one_hour_timer == 1800:
                temp = self.get_temp()
                one_hour_timer = 0

#        while True:
#            offscreen_canvas.Clear()
#            len = graphics.DrawText(offscreen_canvas, font, pos, 10, textColor, my_text)
#            pos -= 1
#            if (pos + len < 0):
#                pos = offscreen_canvas.width

#            time.sleep(0.05)
#            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()

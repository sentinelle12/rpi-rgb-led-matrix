#!/usr/bin/env python

from nhl_scoreboard_data_manager import GameData
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from samplebase import SampleBase
from PIL import Image, ImageDraw, ImageFont
import time
import sys

images_path = "../nhl_matrix/nhl_logos/"


def get_concat_h(im1, h_logo, a_logo):
    dst = Image.new('RGB', (64, 64))
    dst.paste(im1, (0, 0))
    dst.paste(h_logo, (0, 32))
    dst.paste(a_logo, (44, 32))
    return dst


class HockeyScoreboard(SampleBase):
    def __init__(self, *args, **kwargs):
        super(HockeyScoreboard, self).__init__(*args, **kwargs)
#        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default=my_date)

        self.game_data = GameData()
        self.is_there_a_game_tonight = False
        self.game_info = {}
        self.game_live_data = {}

        # self.period_text = object
        # self.home_goals_text = object
        # self.away_goals_text = object
        # self.time_remaining_text = object
        # self.home_shots_text = object
        # self.away_shots_text = object
        # self.powerplay_text = object

        # self.home_img = object
        # self.away_img = object
        self.home_logo = object
        self.away_logo = object
        self.im1 = object
        # self.soiree_hockey_img = object
        # self.soiree_hockey_logo = object

    def run(self):

        # offscreen_canvas = self.matrix.CreateFrameCanvas()

        # # TEAM ABBR FONT
        # font1 = graphics.Font()
        # font1.LoadFont("../../../fonts/6x10.bdf")
        #
        # # GOAL FONTS
        # font2 = graphics.Font()
        # font2.LoadFont("../../../fonts/9x18B.bdf")
        #
        # # SHOTS/PERIOD/TIME REMAINING/DETAILED STATE FONT
        # font3 = graphics.Font()
        # font3.LoadFont("../../../fonts/5x8.bdf")
        #
        # # SMALLER FONT
        # font4 = graphics.Font()
        # font4.LoadFont("../../../fonts/4x6.bdf")
        #
        # blue = graphics.Color(0, 127, 255)
        # red = graphics.Color(175, 30, 45)
        # white = graphics.Color(255, 255, 255)

        fnt1 = ImageFont.truetype('../nhl_matrix/nhl_fonts/arial.ttf', 24)
        fnt2 = ImageFont.truetype('../nhl_matrix/nhl_fonts/arialbd.ttf', 32)

        while True:

            # offscreen_canvas.Clear()

            self.is_there_a_game_tonight = self.game_data.game_tonight()
            print("is_there_a_game_tonight (updated): {}".format(self.is_there_a_game_tonight))

            if self.is_there_a_game_tonight:
                self.game_info = self.game_data.get_game_static_info()
                print("game_info = {}".format(self.game_info))

                # home_logo = Image.open('{}{}r.png'.format(images_path, self.game_info['home_team_abbr']))
                # away_logo = Image.open('{}{}r.png'.format(images_path, self.game_info['away_team_abbr']))

                if self.game_info["abstract_game_state"] == "Live" or self.game_info["abstract_game_state"] == "Final":

                    self.game_live_data = self.game_data.get_live_data()
                    print("game_live_data: {}".format(self.game_live_data))

                    im1 = Image.new('RGB', (64, 64), (0, 0, 0))
                    home_logo = Image.open('{}{}.png'.format(images_path, self.game_info['home_team_abbr']))
                    away_logo = Image.open('{}{}.png'.format(images_path, self.game_info['away_team_abbr']))

                    draw1 = ImageDraw.Draw(im1)
                    draw1.text((24, 32), str(self.game_live_data['home_goals']), font=fnt2, fill=(255,255,255,128))
                    draw1.text((40, 32), str(self.game_live_data['away_goals']), font=fnt2, fill=(255,255,255,128))
                    draw1.text((32, 32), str(self.game_live_data['away_goals']), font=fnt1, fill=(255,255,255,128))

                    im_pil = get_concat_h(im1, home_logo, away_logo)

                    canvas = self.matrix.SetImage(im_pil)
                    canvas = self.matrix.SwapOnVSync(canvas)

                #

                #
                #     home_logo.thumbnail((self.matrix.width / 2.2, self.matrix.height / 2.2), Image.ANTIALIAS)
                #     away_logo.thumbnail((self.matrix.width / 2.2, self.matrix.height / 2.2), Image.ANTIALIAS)
                #
                #     self.matrix.SetImage(home_logo.convert('RGB'), 1, 1)
                #     self.matrix.SetImage(away_logo.convert('RGB'), 1 + home_logo.width + 4, 1)
                #
                #     graphics.DrawText(offscreen_canvas, font1, 5, 10, blue, str(self.game_info['home_team_abbr']))
                #     graphics.DrawText(offscreen_canvas, font1, 42, 10, blue, str(self.game_info['away_team_abbr']))
                #
                #     graphics.DrawText(offscreen_canvas, font3, 20, 20, white, self.game_live_data['current_time_remaining'])
                #
                #     graphics.DrawText(offscreen_canvas, font2, 10, 40, white, str(self.game_live_data['home_goals']))
                #     graphics.DrawText(offscreen_canvas, font2, 49, 40, white, str(self.game_live_data['away_goals']))
                #
                #     graphics.DrawText(offscreen_canvas, font3, 32, 37, blue, str(self.game_live_data['current_period']))
                #
                #     graphics.DrawText(offscreen_canvas, font4, 27, 56, red, "Tirs")
                #     graphics.DrawText(offscreen_canvas, font4, 10, 56, red, str(self.game_live_data['home_shots_on_goal']))
                #     graphics.DrawText(offscreen_canvas, font4, 54, 56, red, str(self.game_live_data['away_shots_on_goal']))
                #
                #     offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                #
                #     time.sleep(30)

            #     elif self.game_info["abstract_game_state"] == "Preview":
            #
            #         graphics.DrawText(offscreen_canvas, font1, 5, 32, blue, "Preview")
            #         offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            #         time.sleep(30)
            #
            # else:
            #     print("display no game")
            #
            #     graphics.DrawText(offscreen_canvas, font1, 5, 32, blue, "No game")
            #     offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            #     time.sleep(3600)



# Main function
if __name__ == "__main__":
    my_matrix = HockeyScoreboard()
    if (not my_matrix.process()):
        my_matrix.print_help()

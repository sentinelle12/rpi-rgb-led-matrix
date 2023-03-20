#!/usr/bin/env python

from nhl_scoreboard_data_manager import GameData
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image
import time
import sys


class NhlLedMatrix:
    def __init__(self, master):
        self.master = master(options=self.options)
        self.options = RGBMatrixOptions()
        self.options.rows = 64
        self.options.cols = 64
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

        # self.game_data = GameData()
        # self.is_there_a_game_tonight = False
        # self.game_info = {}
        # self.game_live_data = {}

        # self.home_img = object
        # self.away_img = object
        # self.home_logo = object
        # self.away_logo = object
        # self.soiree_hockey_img = object
        # self.soiree_hockey_logo = object

        # self.period_text = object
        # self.home_goals_text = object
        # self.away_goals_text = object
        # self.time_remaining_text = object
        # self.home_shots_text = object
        # self.away_shots_text = object
        # self.powerplay_text = object

        self.run()

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font1 = graphics.Font()
        font1.LoadFont("../../../fonts/7x13.bdf")
        blue = graphics.Color(0, 127, 255)

        while True:
            offscreen_canvas.Clear()
            graphics.DrawText(offscreen_canvas, font1, 5, 10, blue, 'Mon panneau !')
            offscreen_canvas = self.master.SwapOnVSync(offscreen_canvas)

    # def update_game_info(self):
    #
    #     self.is_there_a_game_tonight = self.game_data.game_tonight()
    #     print(f"is_there_a_game_tonight (updated): {self.is_there_a_game_tonight}")
    #
    #     if self.is_there_a_game_tonight:
    #         self.game_info = self.game_data.get_game_static_info()
    #         print(f"game_info = {self.game_info}")
    #
    #         if self.game_info["abstract_game_state"] == "Live" or self.game_info["abstract_game_state"] == "Final":
    #             self.game_live_data = self.game_data.get_live_data()
    #             print(f"game_live_data: {self.game_live_data}")
    #             self.display_gamelive_screen()
    #
    #         elif self.game_info["abstract_game_state"] == "Preview":
    #             pass
    #             # self.display_preview_screen()
    #
    #     else:
    #         print("display no game")
    #         self.display_no_game()


my_matrix = NhlLedMatrix(RGBMatrix)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)

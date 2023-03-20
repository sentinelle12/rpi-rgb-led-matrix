import time
from tkinter import *
from PIL import Image, ImageTk
import requests
from datetime import datetime
from data_manager import GameData

FONT_NAME = "Calibri"
def create_transparent_image(filename):

    img = Image.open(filename)
    rgba = img.convert("RGBA")
    datas = rgba.getdata()
    new_data = []
    for item in datas:
        new_data.append((item[0], item[1], item[2], 32))
    rgba.putdata(new_data)
    rgba.save(filename, "PNG")

def resize_logo(filename):

    img = Image.open(filename)
    logo_width = int(img.width/3)
    logo_height = int(img.height/3)
    resized_img = img.resize((logo_width, logo_height), Image.LANCZOS)

    return resized_img

def update_display():
    pass



game_data = GameData()
is_there_a_game_tonight = game_data.game_tonight()
print(is_there_a_game_tonight)

if is_there_a_game_tonight:
    game_info = game_data.get_game_static_info()
    print(f"game_info = {game_info}")

    if game_info["game_detailed_state"] == "In Progress":
        game_live_data = game_data.get_live_data()
        print(game_live_data)

else:
    print("Le Canadiens ne joue pas ce soir.")


# ------------------------ UI SETUP -------------------

window = Tk()
window.title("NHL Game Display")
window.config(padx=5, pady=5, bg='#000000')
window.geometry('640x640')

canvas_width = 640
canvas_height = 640
canvas = Canvas(width=canvas_width, height=canvas_height, bg="#000000", highlightthickness=0)

home_logo = create_transparent_image("./nhl_logos/8.png")
home_logo = resize_logo("./nhl_logos/8.png")
home_logo_width = home_logo.width
home_logo_height = home_logo.height

away_logo = create_transparent_image("./nhl_logos/1.png")
away_logo = resize_logo("./nhl_logos/1.png")
away_logo_width = away_logo.width
away_logo_height = away_logo.height

home_logo = ImageTk.PhotoImage(home_logo)
away_logo = ImageTk.PhotoImage(away_logo)

canvas.create_image(80, 150, image=home_logo)
canvas.create_image(560, 150, image=away_logo)

period = canvas.create_text(320, 100, text="Période : 0", fill="white", font=(FONT_NAME, 16, "normal"))
home_goals_text = canvas.create_text(150, 370, text="0", fill="white", font=(FONT_NAME, 128, "bold"))
away_goals_text = canvas.create_text(490, 370, text="0", fill="white", font=(FONT_NAME, 128, "bold"))
time_remaining_text = canvas.create_text(320, 150, text="20:00", fill="white", font=(FONT_NAME, 32, "normal"))
home_shots_text = canvas.create_text(150, 490, text="Tirs: 0", fill="white", font=(FONT_NAME, 16, "normal"))
away_shots_text = canvas.create_text(490, 490, text="Tirs: 0", fill="white", font=(FONT_NAME, 16, "normal"))

# away_logo = PhotoImage(file="./nhl_logos/EDM.png")
# canvas.create_image(300, 200, image=away_logo)
canvas.grid(column=1, row=1)

window.mainloop()



# TODO - Check if the Canadians are playnig in the current date

""""Endpoint /schedule/ with no date parameter returns schedule of current date.
Pass teamId=8 to see if our home team is playing.

# https://statsapi.web.nhl.com/api/v1/schedule?teamId=8

If call returns "totalGames" : 1, then we know that there's a game scheduled.

From this call, we can also retrieve the following information for future use :

      "gamePk" : 2022020813,
      "link" : "/api/v1/game/2022020813/feed/live",
"""


# TODO - Display time of game on the panel




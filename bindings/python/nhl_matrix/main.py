import tkinter as tk
from PIL import Image, ImageTk
from data_manager import GameData
import cairosvg
import requests

FONT_NAME = "Arial"

# def process_logo(filename):
#
#     # Load SVG data in a variable
#     response = requests.get(filename)
#     response.raise_for_status()
#     svg_data = response.text()
#     # Convert SVG data to PNG format using cairosvg for usage by PIL
#     filelike_obj = io.BytesIO(cairosvg.svg2png(svg_data))
#
#     # Open the image using PIL
#     img = Image.open(filelike_obj)
#
#     rgba = img.convert("RGBA")
#     datas = rgba.getdata()
#     new_data = []
#     for item in datas:
#         new_data.append((item[0], item[1], item[2], 32))
#     rgba.putdata(new_data)
#     new_filename = f"./nhl_logos/{filename[12:15]}r.png"
#     print(f"new_filename : {new_filename}")
#     rgba.save(new_filename, "PNG")


def resize_logo(filename, ratio):
    img = Image.open(filename)
    logo_width = int(img.width / ratio)
    logo_height = int(img.height / ratio)
    processed_img = img.resize((logo_width, logo_height), Image.LANCZOS)

    return processed_img


class nhl_App:
    def __init__(self, master):
        self.master = master
        self.game_data = GameData()
        self.is_there_a_game_tonight = False
        self.game_info = {}
        self.game_live_data = {}

        self.master.title("NHL Game Display")
        self.master.config(padx=5, pady=5, bg='#000000')
        self.master.geometry('640x640')

        self.canvas = tk.Canvas(master, width=640, height=640, bg="#000000", highlightthickness=0)

        self.home_img = object
        self.away_img = object
        self.home_logo = object
        self.away_logo = object
        self.soiree_hockey_img = object
        self.soiree_hockey_logo = object
        self.period_text = object
        self.home_goals_text = object
        self.away_goals_text = object
        self.time_remaining_text = object
        self.home_shots_text = object
        self.away_shots_text = object
        self.powerplay_text = object
        self.update_game_info()

    def update_game_info(self):

        self.is_there_a_game_tonight = self.game_data.game_tonight()
        print(f"is_there_a_game_tonight (updated): {self.is_there_a_game_tonight}")

        if self.is_there_a_game_tonight:
            self.game_info = self.game_data.get_game_static_info()
            print(f"game_info = {self.game_info}")

            if self.game_info["abstract_game_state"] == "Live" or self.game_info["abstract_game_state"] == "Final":
                self.game_live_data = self.game_data.get_live_data()
                print(f"game_live_data: {self.game_live_data}")
                self.display_gamelive_screen()

            elif self.game_info["abstract_game_state"] == "Preview":
                self.display_preview_screen()

        else:
            print("display no game")
            self.display_no_game()

    def display_preview_screen(self):

        self.canvas.delete('all')
        process_logo(f"./nhl_logos/{self.game_info['home_team_abbr']}.png")
        home_logo = resize_logo(f"./nhl_logos/{self.game_info['home_team_abbr']}r.png", 5)
        process_logo(f"./nhl_logos/{self.game_info['away_team_abbr']}.png")
        away_logo = resize_logo(f"./nhl_logos/{self.game_info['away_team_abbr']}r.png", 5)
        self.home_img = ImageTk.PhotoImage(home_logo)
        self.away_img = ImageTk.PhotoImage(away_logo)

        self.home_logo = self.canvas.create_image(80, 320, image=self.home_img)
        self.away_logo = self.canvas.create_image(560, 320, image=self.away_img)
        self.invite_text = self.canvas.create_text(320, 50, text='Ce soir', fill='white',
                                                   font=(FONT_NAME, 54, 'normal'))
        self.vs_text = self.canvas.create_text(320, 320, text='VS', fill='white', font=(FONT_NAME, 72, 'bold'))
        self.game_time = self.canvas.create_text(320, 550, text=f"{self.game_info['adjusted_game_time']}", fill="white",
                                                 font=(FONT_NAME, 54, 'normal'))
        self.canvas.pack()
        self.canvas.update()
        self.master.after(60000, self.update_game_info)

    def display_gamelive_screen(self):

        self.canvas.delete('all')

        # process_logo(f"./nhl_logos/{self.game_info['home_team_abbr']}.png")
        home_logo = resize_logo(f"./nhl_logos/{self.game_info['home_team_abbr']}r.png", 4)
        # process_logo(f"./nhl_logos/{self.game_info['away_team_abbr']}.png")
        away_logo = resize_logo(f"./nhl_logos/{self.game_info['away_team_abbr']}r.png", 4)
        self.home_img = ImageTk.PhotoImage(home_logo)
        self.away_img = ImageTk.PhotoImage(away_logo)

        self.home_logo = self.canvas.create_image(int(self.home_img.width()/2 + 20), 120, image=self.home_img)
        self.away_logo = self.canvas.create_image(int(620 - self.away_img.width()/2), 120, image=self.away_img)

        self.period_text = self.canvas.create_text(320, 300, text=f"Période: {self.game_live_data['current_period']}",
                                                   fill="white", font=(FONT_NAME, 16, "normal"))
        self.home_goals_text = self.canvas.create_text(120, 370, text=self.game_live_data['home_goals'], fill="white", font=(FONT_NAME, 128, "bold"))
        self.away_goals_text = self.canvas.create_text(520, 370, text=self.game_live_data['away_goals'], fill="white", font=(FONT_NAME, 128, "bold"))
        self.time_remaining_text = self.canvas.create_text(320, 370, text=self.game_live_data["current_time_remaining"], fill="white",
                                                           font=(FONT_NAME, 32, "normal"))
        self.home_shots_text = self.canvas.create_text(120, 490, text=f"Tirs: {self.game_live_data['home_shots_on_goal']}", fill="white",
                                                       font=(FONT_NAME, 16, "normal"))
        self.away_shots_text = self.canvas.create_text(520, 490, text=f"Tirs: {self.game_live_data['away_shots_on_goal']}", fill="white",
                                                       font=(FONT_NAME, 16, "normal"))
        # self.detailed_state_text = self.canvas.create_text(320, 550, text=self.game_live_data['detailed_state'], fill="light blue",
        #                                               font=(FONT_NAME, 16, "normal"))
        self.canvas.pack()
        self.canvas.update()
        self.master.after(30000, self.update_game_info)


    def display_no_game(self):
        self.canvas.delete('all')
        self.soiree_hockey_img = resize_logo(f"./nhl_logos/soiree_hockey.png", 4)
        self.soiree_hockey_img = ImageTk.PhotoImage(self.soiree_hockey_img)
        self.soiree_hockey_logo = self.canvas.create_image(320, 320, image=self.soiree_hockey_img)
        self.no_game_text = self.canvas.create_text(320, 140, text="Pas de partie aujourd\'hui",
                                                    fill='white',
                                                    font=(FONT_NAME, 24, 'bold'))
        self.canvas.pack()
        self.canvas.update()
        self.master.after(3600000, self.update_game_info)


root = tk.Tk()
myapp = nhl_App(root)
root.mainloop()

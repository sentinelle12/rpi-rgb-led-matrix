import requests
from datetime import datetime

API_URL = "https://statsapi.web.nhl.com"
schedule_end_point = "/api/v1/schedule"

class GameData:
    def __init__(self):
        self.schedule_params = {}
        self.home_team_abbr = ""
        self.away_team_abbr = ""
        self.home_team_id = 0
        self.away_team_id = 0
        self.game_time = ""
        self.time_offset = 0
        self.game_link = ""
        self.home_goals= 0
        self.away_goals = 0
        self.home_shots_on_goal = 0
        self.away_shots_on_goal = 0
        self.current_period = 0
        self.current_time_remaining = ""
        self.abstract_game_state = ""
        self.adjusted_game_time = ""

    def game_tonight(self):

        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')
        self.schedule_params = {'teamId': 8, 'date': current_date}

        response = requests.get(f"{API_URL}{schedule_end_point}", params=self.schedule_params)
        response.raise_for_status()
        data = response.json()
        print(data)

        try:
            game_date = data['dates'][0]['games'][0]['gameDate']
            self.game_time = game_date[11:16]
            self.game_link = data["dates"][0]["games"][0]["link"]
            print(self.game_link)
            return True
        except IndexError:
            return False

    def get_game_static_info(self):

        response = requests.get(f"{API_URL}{self.game_link}")
        response.raise_for_status()
        data = response.json()

        self.abstract_game_state= data["gameData"]["status"]["abstractGameState"]
        self.game_time= data["gameData"]["datetime"]["dateTime"][11:16]
        self.home_team_abbr= data["gameData"]["teams"]["home"]["abbreviation"]
        self.away_team_abbr= data["gameData"]["teams"]["away"]["abbreviation"]
        self.home_team_id= data["gameData"]["teams"]["home"]["id"]
        self.away_team_id= data["gameData"]["teams"]["away"]["id"]
        self.time_offset= data["gameData"]["teams"]["home"]["venue"]["timeZone"]["offset"]

        # CALCULATE GAME TIME WITH TIME OFFSET
        self.adjusted_game_time = f"{str(int(self.game_time[0:2]) + int(self.time_offset))}:{self.game_time[-2:]}"

        return {
            "abstract_game_state": self.abstract_game_state,
            "adjusted_game_time": self.adjusted_game_time,
            "home_team_abbr": self.home_team_abbr,
            "away_team_abbr": self.away_team_abbr,
            "home_team_id": self.home_team_id,
            "away_team_id": self.away_team_id,
            "time_offset": self.time_offset,
        }

    def get_live_data(self):
        response = requests.get(f"{API_URL}{self.game_link}")
        response.raise_for_status()
        data = response.json()

        self.detailed_state = data["gameData"]["status"]["detailedState"]
        self.current_period = data["liveData"]["linescore"]["currentPeriod"]
        self.current_time_remaining = data["liveData"]["linescore"]["currentPeriodTimeRemaining"]
        self.home_goals = data["liveData"]["linescore"]["teams"]["home"]["goals"]
        self.away_goals = data["liveData"]["linescore"]["teams"]["away"]["goals"]
        self.home_shots_on_goal = data["liveData"]["linescore"]["teams"]["home"]["shotsOnGoal"]
        self.away_shots_on_goal = data["liveData"]["linescore"]["teams"]["away"]["shotsOnGoal"]

        return {
            "detailed_state": self.detailed_state,
            "current_period": self.current_period,
            "current_time_remaining": self.current_time_remaining,
            "home_goals": self.home_goals,
            "away_goals": self.away_goals,
            "home_shots_on_goal": self.home_shots_on_goal,
            "away_shots_on_goal": self.away_shots_on_goal,
        }


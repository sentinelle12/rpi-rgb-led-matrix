import requests
from datetime import datetime

API_URL = "https://api-web.nhle.com"
schedule_end_point = "/v1/club-schedule-season"
gamecenter_end_point = "/v1/gamecenter/"
gamecenter_view = "/play-by-play"
club_abbr = "MTL"
current_season = "20242025"
mtl_UTCOffset = -4



class GameData:
    def __init__(self):
        self.schedule_params = ""
        self.home_team_abbr = ""
        self.away_team_abbr = ""
        self.home_team_id = 0
        self.away_team_id = 0
        self.game_time = ""
        self.game_id = ""
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
        self.home_logo_link = ""
        self.away_logo_link = ""

    def game_tonight(self):

        now = datetime.now()
        current_date = now.strftime('%Y-%m-%d')

        response = requests.get(f"{API_URL}{schedule_end_point}/{club_abbr}/{current_season}")
        response.raise_for_status()
        data = response.json()

        try:
            game_dates = [data['games'][i]['gameDate'] for i in range(0, len(data['games']) - 1)]
            tonight_game_index = game_dates.index(current_date)
            self.game_time = data['games'][tonight_game_index]['startTimeUTC'][11:16]
            self.game_id = data['games'][tonight_game_index]['id']
            self.home_logo_link = data['games'][tonight_game_index]['home']['logo']
            self.away_logo_link = data['games'][tonight_game_index]['away']['logo']
            return True

        except IndexError:
            return False

    def get_game_static_info(self):

        response = requests.get(f"{API_URL}{gamecenter_end_point}{self.game_id}{gamecenter_view}")
        response.raise_for_status()
        data = response.json()

        self.abstract_game_state = data["gameState"]
        self.game_time = data["startTimeUTC"][11:16]
        self.home_team_abbr = data["homeTeam"]["abbrev"]
        self.away_team_abbr = data["awayTeam"]["abbrev"]
        self.home_team_id = data["homeTeam"]["id"]
        self.away_team_id = data["awayTeam"]["id"]
        self.time_offset = data["easternUTCOffset"][0:3]

        # CALCULATE GAME TIME WITH TIME OFFSET
        self.adjusted_game_time = f"{str(int(game_time[0:2]) + int(time_offset))}:{game_time[-2:]}"

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
        response = requests.get(f"{API_URL}{gamecenter_end_point}{self.game_id}{gamecenter_view}")
        response.raise_for_status()
        data = response.json()
        # print(data)

        self.current_period = data["displayPeriod"]
        self.current_time_remaining = data["clock"]["timeRemaining"]
        self.home_goals = data["homeTeam"]["score"]
        self.away_goals = data["awayTeam"]["score"]
        self.home_shots_on_goal = data["homeTeam"]["sog"]
        self.away_shots_on_goal = data["awayTeam"]["sog"]

        return {
            "current_period": self.current_period,
            "current_time_remaining": self.current_time_remaining,
            "home_goals": self.home_goals,
            "away_goals": self.away_goals,
            "home_shots_on_goal": self.home_shots_on_goal,
            "away_shots_on_goal": self.away_shots_on_goal,
        }


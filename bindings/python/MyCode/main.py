import requests

API_URL = "https://statsapi.web.nhl.com/api/v1/schedule"
schedule_end_point = "/schedule"

# TODO - Check if the Canadians are playnig in the current date

""""Endpoint /schedule/ with no date parameter returns schedule of current date. 
Pass teamId=8 to see if our home team is playing. 

# https://statsapi.web.nhl.com/api/v1/schedule?teamId=8

If call returns "totalGames" : 1, then we know that there's a game scheduled.

From this call, we can also retrieve the following information for future use : 

      "gamePk" : 2022020813,
      "link" : "/api/v1/game/2022020813/feed/live",
"""

schedule_parameters = {'teamId': 8, 'date': '2023-02-12'}


def get_schedule():
    tonight_teamId = []

    response = requests.get(API_URL, params=schedule_parameters)
    response.raise_for_status()
    data = response.json()
    print(data)

    if data["totalGames"] == 0:
        print("Sorry. No game tonight!")

    else:
        game_date = data['dates'][0]['games'][0]['gameDate']
        game_time = game_date[11:16]
        time_zone = game_date[17:20]

        game_key = data["dates"][0]["games"][0]["gamePk"]
        game_link = data["dates"][0]["games"][0]["link"]

        abstract_game_state = data["dates"][0]["games"][0]["status"]["abstractGameState"]

        home_team_name = data["dates"][0]["games"][0]["teams"]["home"]["team"]["name"]
        away_team_name = data["dates"][0]["games"][0]["teams"]["away"]["team"]["name"]

        home_team_id = data["dates"][0]["games"][0]["teams"]["home"]["team"]["id"]
        away_team_id = data["dates"][0]["games"][0]["teams"]["away"]["team"]["id"]

        print(f"game_date:{game_date}\n"
              f"game_time: {game_time}\n"
              f"time_zone: {time_zone}\n"
              f"game_key: {game_key}\n"
              f"game_link: {game_link}\n"
              f"home_team_id: {home_team_id}\n"
              f"home_team_name: {home_team_name}\n"
              f"away_team_name: {away_team_name}\n"
              f"away_team_id: {away_team_id}\n"
              f"abstract_game_state: {abstract_game_state}\n\n"
              f"commence à {game_time}")

        if abstract_game_state == "live":
            get_live_results()


def get_live_results():

    is_live = True

    while is_live:



get_schedule()

# TODO - Display time of game on the panel


# TODO - Get live information of the game in progress
""" Once in the live feed endpoint, we can get the about section of the response.

"about": {
    "eventIdx": 345,
    "eventId": 1089,
    "period": 4,
    "periodType": "OVERTIME",
    "ordinalNum": "OT",
    "periodTime": "01:21",
    "periodTimeRemaining": "03:39",
    "dateTime": "2023-02-08T02:40:56Z",
    "goals": {
        "away": 1,
        "home": 1
}

"""

import os
import requests


def find_close_games():
    '''Finds close games for given wnba team'''
    res = requests.get('https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard')
    print(res.status_code)
    res = res.json()

    for event in res["events"]:
        competition = event["competitions"][0]

        for competitor in competition["competitors"]:
            team = competitor["team"]

            if team['id'] == os.getenv('WNBA_ID'):
                print("Hell yea")
                scores = []
                for competitor in competition['competitors']:
                    scores.append(competitor['score'])
                scoreDif = abs(int(scores[0]) - int(scores[1]))
                print(scoreDif)
                status = competition["status"]

                clock = status["displayClock"]
                period = status["period"]
                status_type = status['type']

                if status_type['name'] != "STATUS_FINAL" and period > 3 and float(clock) <= 300:
                    print("CLOSE GAME for chosen team")

                send_text()
                save_game(event["id"])

def send_text():
    '''Send text message to phone save in env var'''
    pass

def save_game():
    '''Save event id to db to prevent multiple texts'''
    pass
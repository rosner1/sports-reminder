import os
import requests
import boto3

WNBA_URL = 'https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard'
NBA_URL = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard'
URLS = [WNBA_URL, NBA_URL]

def clock_to_seconds(clock):
    minutes, seconds = clock.split(":")
    return int(minutes) * 60 + int(seconds)

def find_close_games():
    '''Finds close games for given wnba team'''

    for url in URLS:
        res = requests.get(url)
        print(res.status_code)
        res = res.json()

        for event in res["events"]:
            competition = event["competitions"][0]

            for competitor in competition["competitors"]:
                team = competitor["team"]

                if (url == WNBA_URL and team['id'] == os.getenv('WNBA_ID')) or (url == NBA_URL and team['id'] == os.getenv('NBA_ID')):
                    print("Hell yea")
                    scores = []
                    for competitor in competition['competitors']:
                        scores.append(competitor['score'])
                    scoreDif = abs(int(scores[0]) - int(scores[1]))
                    print(scoreDif)
                    status = competition["status"]

                    clock = status["displayClock"]
                    remaining_seconds = clock_to_seconds(clock)
                    period = status["period"]
                    status_type = status['type']

                    if status_type['name'] != "STATUS_FINAL" and period >= 3 and float(remaining_seconds) <= 300 and scoreDif <= 15:
                        print("CLOSE GAME for chosen team")

                    send_text()
                    save_game(event["id"])

def send_text():
    '''Send text message to phone save in env var'''
    pass

def save_game(id):
    '''Save event id to db to prevent multiple texts'''
    pass

find_close_games()
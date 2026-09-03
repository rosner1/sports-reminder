import os
import requests
import boto3

WNBA_URL = 'https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard'
NBA_URL = 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard'
URLS = [WNBA_URL, NBA_URL]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
ses = boto3.client("ses", region_name="us-east-2")

def clock_to_seconds(clock):
    if not clock or ":" not in clock:
        return 0

    minutes, seconds = clock.split(":")
    return int(minutes) * 60 + int(seconds)

def find_close_games():
    '''Finds close games for given wnba and nba team'''

    for url in URLS:
        res = requests.get(url)

        print(f"URL: {url}")
        print(f"Status code: {res.status_code}")
        print(f"Response: {res.text[:500]}")

        res.raise_for_status()
        res = res.json()

        for event in res["events"]:
            res = table.get_item(
                Key={
                    "eventId": event["id"]
                }
            )
            if "Item" in res:
                continue
                

            competition = event["competitions"][0]


            for competitor in competition["competitors"]:
                team = competitor["team"]

                if (url == WNBA_URL and team['id'] == os.getenv('WNBA_ID')) or (url == NBA_URL and team['id'] == os.getenv('NBA_ID')):
                    scores = []
                    for competitor in competition['competitors']:
                        scores.append(competitor['score'])
                    scoreDif = abs(int(scores[0]) - int(scores[1]))
                    status = competition["status"]

                    clock = status["displayClock"]
                    remaining_seconds = clock_to_seconds(clock)
                    period = status["period"]
                    status_type = status['type']

                    if status_type['name'] != "STATUS_FINAL" and period > 3 and float(remaining_seconds) <= 300 and scoreDif <= 6:
                        send_email(team["displayName"])
                        save_game(event["id"])

def send_email(team):
    '''Send email to yourself from env var'''
    response = ses.send_email(
        Source=os.environ["EMAIL_ADDRESS"],
        Destination={
            "ToAddresses": [os.environ["EMAIL_ADDRESS"]]
        },
        Message={
            "Subject": {
                "Data": f"{team} Close Game"
            },
            "Body": {
                "Text": {
                    "Data": f"The {team} are in a close gme!"
                }
            }
        }
    )

def save_game(id):
    '''Save event id to db to prevent multiple texts'''
    table.put_item(
        Item={
            "eventId": id
        }
    )

def lambda_handler(event, context):
    find_close_games()

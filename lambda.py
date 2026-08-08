import os
import requests

res = requests.get('https://site.api.espn.com/apis/site/v2/sports/basketball/wnba/scoreboard')
print(res.status_code)
res = res.json()

for event in res["events"]:
    competition = event["competitions"][0]

    for competitor in competition["competitors"]:
        team = competitor["team"]

        print({
            "event_id": event["id"],
            "team_id": team["id"],
            "team": team["displayName"],
            "abbreviation": team["abbreviation"],
            "score": int(competitor["score"]),
            "home_away": competitor["homeAway"],
        })
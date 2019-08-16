import tweepy
import time
import requests
import os
from bs4 import BeautifulSoup

API_KEY = ""
API_SECRET_KEY = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Placeholder id = 1060682754885648389

FILE_NAME = 'seen_ids.txt'

def get_last_seen_id(filename):
    file_read = open(filename, 'r')
    last_seen = int(file_read.read().strip())
    file_read.close()
    return last_seen

def store_last_seen_id(last_seen, filename):
    file_write = open(filename, 'w')
    file_write.write(str(last_seen))
    file_write.close()
    return

def reply():
    print("Replying...", flush=True)
    lastSeenId = get_last_seen_id(FILE_NAME)

    # Get the list of recent mentions
    mentions = api.mentions_timeline(lastSeenId, tweet_mode='extended')
    print("Received mentions...", flush=True)
    for m in reversed(mentions):
        print("Inspecting the mention...", flush=True)
        lastSeenId = m.id
        store_last_seen_id(lastSeenId, FILE_NAME)
        if '#golazo' in m.full_text.lower():

            scrape_url = "https://www.livescores.com/"
            print("Scraping match details...")

            try:
                livescores = requests.get(scrape_url)
            except Exception as e:
                print(f'Error occured as {e}')

            parsed = BeautifulSoup(livescores.text, 'html.parser')

            scores = []
            matches = []
            timings = []

            for element in parsed.find_all("div", "row-gray"):
                home = ' '.join(element.find("div", "tright").get_text().strip().split(" "))
                away = ' '.join(element.find(attrs = {"class": "ply name"}).get_text().strip().split(" "))
                match_time = ' '.join(element.find("div", "min").get_text().strip().split(" "))

                home_score = element.find("div", "sco").get_text().split("-")[0].strip()
                away_score = element.find("div", "sco").get_text().split("-")[1].strip()

                matches.append(f'{home} vs {away}')
                scores.append(f'{home_score} - {away_score}')
                timings.append([f'{match_time}'])

            game1 = matches[0] + '\n' + "Game Time: " + timings[0][0] + '\n' + "Score: " + scores[0] + '\n' + '\n'
            game2 = matches[1] + '\n' + "Game Time: " + timings[1][0] + '\n' + "Score: " + scores[1] + '\n' + '\n'
            game3 = matches[2] + '\n' + "Game Time: " + timings[2][0] + '\n' + "Score: " + scores[2] + '\n'

            tweet = game1 + game2 + game3 + "#PynenkaLiveScores #Football #TheBeautifulGame"
            api.update_status('@' + m.user.screen_name + " " + tweet, m.id)
        print('replied')
    print('exit mentions')

while True:
    reply()
    time.sleep(30)      



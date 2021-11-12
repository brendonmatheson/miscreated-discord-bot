
from os.path import exists
import json
import requests

webhook_url = "TODO"
dry_run = False

#
# Pull stats from Miscreated
#

aus1_url = "https://servers.miscreatedgame.com/api/get-server/109.200.214.230:64122"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
	"Accept": "application/json",
	"Accept-Language": "en-US,en;q=0.5",
	"Origin": "https://servers.miscreatedgame.com",
	"DNT": "1",
	"Connection": "keep-alive",
	"Referer": "https://servers.miscreatedgame.com/",
	"Sec-Fetch-Dest": "empty",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Site": "same-origin",
	"Content-Length": "0",
	"TE": "trailers"
	}

result = requests.post(aus1_url, data=json.dumps(headers))

weather_names = {
	"ClearSky": "Clear Sky"
}

got_data = False
data = None
day = False
weather = None
num_players = 0
time = None

if (result.status_code) == 200:
	#print "Success"
	#print(str(result.content))

	data = json.loads(result.content)

	day = "Yes" if data["day"] else "No"
	weather = data["weather"]
	if weather in weather_names:
		weather = weather_names[weather]
	num_players = data["numPlayers"]
	time = data["time"]

	got_data = True

change_detected = False
message = None

if got_data:
	last_num_players = -1
	if exists("/tmp/miscreated_data.txt"):
		# Check last num_players
		f = open("/tmp/miscreated_data.txt", "r")
		last_data_content = f.read()
		#print("last_data_content: " + last_data_content)
		last_data = json.loads(last_data_content)
		f.close()

		last_num_players = last_data["numPlayers"]
		#print("last_num_players: " + str(last_num_players))

	message_required = num_players != last_num_players and (num_players == 0 or last_num_players == 0)

	if message_required:
		message = {
			"username": "HAL8000",
			"content": "AUS1 update.  Players: " + str(num_players) + "; Weather: " + weather + "; Daytime: " + day + ";" # Time: " + time + ";"
			}

		# Update last num_players
		f = open("/tmp/miscreated_data.txt", "a")
		f.write(json.dumps(data))
		f.close()

		change_detected = True

#
# Publish to Discord
#

if change_detected:
	if dry_run:
		print("Posting message: " + str(message))

	else:
		requests.post(
			webhook_url,
			json=message)



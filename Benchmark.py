import os
import time
import subprocess
import json
import os

P1 = "Bot.py"
P2 = "StarterBot.py"

player_1_wins = 0
player_2_wins = 0
MAX_RUNS = 20
for num in range(MAX_RUNS):
    try:
        #print("Currently on: {}".format(num))
        if player_1_wins > 0 or player_2_wins > 0:
            p1_pct = round(player_1_wins/(player_1_wins+player_2_wins)*100.0, 2)
            p2_pct = round(player_2_wins/(player_1_wins+player_2_wins)*100.0, 2)
            print("Player 1 win: {}%; Player 2 win: {}%.".format(p1_pct, p2_pct))
        result = subprocess.run(['./halite','--replay-directory','replays/','--results-as-json','--width 16','--height 16',"python3 "+P1,"python3 "+P2], stdout=subprocess.PIPE)
        resultsJson = result.stdout.decode('utf8')
        data = json.loads(resultsJson)
        stats = data['stats']
        #print("Bot Rank: {} Score: {}".format(stats["0"]["rank"],stats["0"]["score"]))
        #print("StarterBot Rank: {} Score: {}".format(stats["1"]["rank"],stats["1"]["score"]))

        if stats["0"]["rank"] == 1:
            #print("Bot won")
            player_1_wins += 1

        elif stats["1"]["rank"] == 1:
            #print("Starter won")
            player_2_wins += 1
    except Exception as e:
        print(str(e))
        time.sleep(2)

if player_1_wins > 0 or player_2_wins > 0:
    p1_pct = round(player_1_wins/(player_1_wins+player_2_wins)*100.0, 2)
    p2_pct = round(player_2_wins/(player_1_wins+player_2_wins)*100.0, 2)
    print("Player 1 win: {}%; Player 2 win: {}%.".format(p1_pct, p2_pct))

dir_name = "/home/stormix/Desktop/Halite3/Bot/"
test = os.listdir(dir_name)

for item in test:
    if item.endswith(".log"):
        os.remove(os.path.join(dir_name, item))
    if item.endswith(".hlt"):
        os.remove(os.path.join(dir_name, item))
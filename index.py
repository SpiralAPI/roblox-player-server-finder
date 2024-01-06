#   @author:SpiralAPI
#   @description: Search users badges and popular roblox games to locate and track which game a roblox player is playing.
#   @date: 5/2/2023

#==IMPORTS==
import requests
import os
import sys
import json
import subprocess 

#==FUNCTIONS==
def GetID(Username): # Retrieves userid via a username
    resp = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [Username], "excludeBannedUsers": True})

    if resp.json()["data"][0]["id"]:
        return resp.json()["data"][0]["id"]

    return None

def GetRecentBadge(UserID): # retrieves 10 most recent badges via a userid
    resp = requests.get(f"https://badges.roblox.com/v1/users/{UserID}/badges?limit=10&sortOrder=Desc")

    try:
        return resp.json()["data"][0]["id"]
    except:
        return None
    
def GetGameFromBadge(BadgeID): # retrives the game a badge belongs to
    resp = requests.get(f"https://badges.roblox.com/v1/badges/{BadgeID}")

    try:
        return resp.json()["awardingUniverse"]["name"], resp.json()["awardingUniverse"]["rootPlaceId"]
    except:
        return None, None
    
def GetServers(GameID): # gets all servers in a game
    cursor = ""
    complete = False

    finalReturn = list()

    while (complete == False):
        response = requests.get(f"https://games.roblox.com/v1/games/{GameID}/servers/Public?limit=100&cursor={cursor}")
        data = response.json()["data"]

        if ((response.json()["nextPageCursor"] == "null") or (response.json()["nextPageCursor"] == None) or (response.json()["nextPageCursor"] == "None")):
            complete = True
        else:
            complete = False
            cursor = response.json()["nextPageCursor"]
        
        for server in data:
            finalReturn.append(server)

    return finalReturn

def CopyToClipboard(txt): # self explanatory
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)
    
def FindUserInGame(UserID, GameID): # the main function. searches all servers in a game for a user (using their headshot)
    targetThumb = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={UserID}&size=150x150&format=Png&isCircular=false").json()["data"][0]["imageUrl"]

    servers = GetServers(GameID)

    for server in servers:
        for token in server["playerTokens"]:
            data = []
            data.append({
                "format": "png",
                "requestId": f"0:{token}:AvatarHeadshot:150x150:png:regular",
                "size": "150x150",
                "targetId": 0,
                "token": token,
                "type": "AvatarHeadShot",
                })
            
        temp = requests.post(f"https://thumbnails.roblox.com/v1/batch", headers = {"Content-Type": "application/json"}, data = json.dumps(data))
        try:
            for thumb in temp.json()['data']:
                userThumb = thumb["imageUrl"]
                if userThumb == targetThumb:
                    print("Server found")
                    return server

            print(f"Searching server ({servers.index(server)}/{len(servers)})")
        except:
            print(f"Failed searching server #{servers.index(server)}")
    
    return None

def clearConsole(): # purely visuals
    os.system('cls' if os.name=='nt' else 'clear')
    print("""
:'######::'########::'####:'########:::::'###::::'##::::::::
'##... ##: ##.... ##:. ##:: ##.... ##:::'## ##::: ##::::::::
 ##:::..:: ##:::: ##:: ##:: ##:::: ##::'##:. ##:: ##::::::::
. ######:: ########::: ##:: ########::'##:::. ##: ##::::::::
:..... ##: ##.....:::: ##:: ##.. ##::: #########: ##::::::::
'##::: ##: ##::::::::: ##:: ##::. ##:: ##.... ##: ##::::::::
. ######:: ##::::::::'####: ##:::. ##: ##:::: ##: ########::
:......:::..:::::::::....::..:::::..::..:::::..::........:::
:::::::::::::::::ROBLOX PLAYER SERVER FINDER::::::::::::::::\n\n
""")

#==FUNCTIONALITY==
clearConsole()

targetValid = False
targetID = 0
while (targetValid == False): # inputs for an easy to use program
    user = input("Please enter your targets username (type 'exit' to quit): ")
    if user == "exit":
        clearConsole()
        sys.exit("Quitting program.")
    else:
        id = GetID(user) 
        if id != None:
            targetValid = True
            targetID = id
        else:
            print("Invalid user. Please try again.")

clearConsole()

badgeID = GetRecentBadge(targetID)

# checks for if the program could not run 
if badgeID == None:
    sys.exit("Could not fetch badge.")

GameName, GameId = GetGameFromBadge(badgeID)

if GameName == None or GameId == None:
    sys.exit("Could not fetch game from badge.")

ServerInfo = FindUserInGame(targetID, GameId)

if ServerInfo == None:
    sys.exit("Could not find user in any games.")

link = f"Roblox.GameLauncher.joinGameInstance({GameId}, '{ServerInfo['id']}')" # the link to join their server

clearConsole()

CopyToClipboard(link)

# the final message
input(f"User was found in {GameName}. \n\nTo join this user, press any key. A line of code will be copied automatically, or you can copy it manually below. Paste the code in your inspect element console at https://roblox.com \n\nCODE: {link}")


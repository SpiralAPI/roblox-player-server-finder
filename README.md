# roblox-player-server-finder
searches players most recent known played game (via most recent obtained badge) to find their server.  

# how it works
it obtains the players badges and locates the most recently obtained badge. afterwards it will loop through the badges respective games servers to find the thumbnail of your target in one of the servers of the game, and it will then provide code you can run on the ROBLOX.com website to launch the ROBLOX player and join their server!

# usage
only non-native python library used is "requests", you can install easily by running pip install requests

simply run and enter the targets username

# safety
the script only contacts official roblox endpoints and wont any data, but if you wanna be safe you can look through the code (good on you for being cautious)

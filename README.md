# Discord Gambling
This is a simple Discord bot that I created on a [Youtube stream](https://www.youtube.com/watch?v=M_WgHeQ_bSU) for one of my viewers. To request your own program to be made on stream, join my Discord server [here](https://discord.gg/kzAtEH6), and send a message in the `#video-requests` channel.

# Setup
To set this bot up for yourself, follow these steps:
 1. Download this project.
 1. Install Python (I used 3.8.2) `MAKE SURE YOU HAVE THE PIP TOOL INSTALLED AND ADD PYTHON TO PATH (environment variables)`
 1. Open a terminal/command prompt in the project folder.
 1. Run `pip install -r requirements.txt`
 1. Create an environment variable called `GamblingToken` and set it to your bot's token.
 1. Change line `14` in `main.py` to have your log channel id.
 1. Run `python main.py`.

# Usage
Here is a list of commands you can use:
  - `example <arg1> [arg2]` - example if the command name, arguments in `<>` are required, and arguments in `[]` are optional. This command would look like `?example arg1` or `?example arg1 arg2` if used.
  - General:
    - `prefix <prefix>` - Change the bot's prefix.
    - `restart` - Restart the bot. Only works if the bot is run using the `Start.bat` file.
  - Gambling:
    - `beg` - Get a random number of coins between 1 and 100. Set on a 2 hour cooldown.
    - `coins [user]` - List the number of coins you have. Include someone's username or mention them to see their coins.
    - `leaderboard` - Show the leaderboard for the coins, and your rank on the server.
    - `gamble <amount>` - Gamble an amount of coins. You have a 48% chance of losing that amount, 48% chance of winning that amount, and 4% chance of hitting the jackpot, which gives you 5 times that amount.
    - `dual <amount> <user>` - Duel a user for coins. Both of you pitch in the same amount of coins, and the winner takes all. Both sides have a 50% chance of winning.

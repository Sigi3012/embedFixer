import discord
from discord.ext import commands
import helpers.checks as checks
from helpers.configSetup import Config
from helpers.setup import setupBot
import signal
import platform
import sys
import os

# --------- #

config = Config.getMainInstance()

class embedFixer(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = "-",
            intents = discord.Intents().all()
        )
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            syncedCommands = await self.tree.sync()
            self.synced = True
        
        print(f"Logged in as {self.user.name}")
        print(f"Python version: {str(platform.python_version())}")
        print(f"Discord.py version: {discord.__version__}")
        print(f"Synced {str(len(syncedCommands))} commands")
        for key, value in vars(config).items():
            print(f"{key}: {value}")
        
    async def setup_hook(self):
        for ext in os.listdir("./cogs"):
            if ext.endswith(".py"):
                await self.load_extension(f"cogs.{ext[:-3]}")

client = embedFixer()

# --------- #

# This is so messy lol
def tests():
    if config.docker != True:
        if checks.check() == False:
            if config.firstRun == True:
                setupBot()
            else:
                exit()
        else:
            pass
    else:
        pass

# --------- #

if __name__ == "__main__":
    tests()
    config.load()
    client.run(config.token)

def signal_handler(filler, filler2):
    print("\n\nImproper shutdown please use /shutdown instead.")
    config.save()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

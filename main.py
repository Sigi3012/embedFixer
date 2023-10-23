import discord
from discord import app_commands
import json
import time
import re

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def currentTime():
    return time.strftime("%H:%M:%S", time.localtime())

with open("config.json", "r") as file:
    config = json.load(file)
    
@tree.command(
    name = "toggle",
    description = "This enables or disables the fixer")
@app_commands.checks.has_permissions(administrator=True)
async def togglefixer(interaction):
    config['enabled'] = not config['enabled']
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    await interaction.response.send_message(f"Toggled to {config['enabled']}", ephemeral=True)
    print(f"Toggled to: {config['enabled']}@{currentTime()}")
@tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You dont have permissions to do this!", ephemeral=True)
    
@tree.command(name= "shutdown", description = "turns off the bot!")
@app_commands.checks.has_permissions(administrator=True)
async def shutdown(interaction):
    await interaction.response.send_message("Shutting down...", delete_after=3.0, ephemeral=True)
    print(f"Bot offline@{currentTime()}")
    await client.close()
@tree.error
async def on_app_command_error(interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("You dont have permissions to do this!", ephemeral=True)

@client.event
async def on_ready():
    await tree.sync()
    print(f"Online!@{currentTime()}")
    print(f"Config loaded!@{currentTime()}")

if __name__ == "__main__":    
    client.run(config["token"])
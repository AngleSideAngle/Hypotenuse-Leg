import os

import discord
from discord.ext import commands

from secrets import token
from settings import command_prefix
from util import EmbedHelp, perm_check, response

intents = discord.Intents.all()
mentions = discord.AllowedMentions(everyone=False, roles=False)
client = commands.Bot(
    command_prefix=command_prefix,
    intents=intents,
    allowed_mentions=mentions,
    help_command=EmbedHelp())

# talking channel : receiving channel
client.connections = {}


# activates all cogs on startup
def load_cogs():
    '''
    loads cogs into the bot
    '''
    for file in os.listdir(os.path.dirname(__file__) + "/cogs"):
        if file.endswith(".py"):
            client.load_extension(f"cogs.{file[:-3]}")


@client.command()
@perm_check()
async def reload(ctx):
    for file in os.listdir(os.path.dirname(__file__) + "/cogs"):
        if file.endswith(".py"):
            client.reload_extension(f"cogs.{file[:-3]}")
    await response(messageable=ctx, text="reloaded cogs")

if __name__ == "__main__":
    load_cogs()
    client.run(token)

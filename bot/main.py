import discord
from discord.ext import commands

import os

from secrets import token
from settings import command_prefix, error_responses, message_error

from utilities.functions import perm_check
from utilities.ErrorCheck import ErrorCheck

intents = discord.Intents.all()
mentions = discord.AllowedMentions(everyone = False, roles = False)
client = commands.Bot(command_prefix = command_prefix, intents = intents, allowed_mentions = mentions)

client.errors = ErrorCheck(error_responses, message_error= message_error)
client.connections = {} # talking channel : receiving channel

#activates all cogs on startup
def load_cogs():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.load_extension(f"cogs.{file[:-3]}")

@client.event
async def on_command_error(ctx, error):
    await client.errors.check(messagable = ctx, author = ctx.author, error = error)

@client.command()
@perm_check()
async def reload(ctx):
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            client.reload_extension(f"cogs.{file[:-3]}")
    await ctx.send("reloaded cogs")

if __name__ == "__main__":
    load_cogs()
    client.run(token)
#!/usr/bin/env python3

import asyncio
from json import load
import os

import discord
from discord.ext import commands

from secret import token
from settings import command_prefix
from util import EmbedHelp, perm_check, response

intents = discord.Intents.all()
mentions = discord.AllowedMentions(everyone=False, roles=False)
bot = commands.Bot(
    command_prefix=command_prefix,
    intents=intents,
    allowed_mentions=mentions,
    help_command=EmbedHelp())

# talking channel : receiving channel
bot.connections = {}


# activates all cogs on startup
async def load_cogs():
    '''
    loads cogs into the bot
    '''
    for file in os.listdir(os.path.dirname(__file__) + "/cogs"):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")


@bot.command()
@perm_check()
async def reload(ctx):
    for file in os.listdir(os.path.dirname(__file__) + "/cogs"):
        if file.endswith(".py"):
            await bot.reload_extension(f"cogs.{file[:-3]}")
    await response(messageable=ctx, text="reloaded cogs")


async def main():
    async with bot:
        await load_cogs()
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())

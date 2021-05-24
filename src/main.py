import discord
#from discord import guild
#from discord.channel import DMChannel, TextChannel
from discord.errors import HTTPException
from discord.ext import commands
from discord.mentions import AllowedMentions
from discord.utils import get

import os

from secrets import token, link
from settings import color, playing, command_prefix, comment_prefix, error_responses, message_error

from utilities.ErrorCheck import ErrorCheck
from utilities.permissions import perm_check, trusted

intents = discord.Intents.default()
intents.members = True

mentions = discord.AllowedMentions(everyone = False, roles = False, replied_user= False)
client = commands.Bot(command_prefix = command_prefix, intents = intents, allowed_mentions = mentions)

#activates all cogs on startup
for file in os.listdir("./src/cogs"):
    if file.endswith(".py"):
        client.load_extension(f"cogs.{file[:-3]}")

command_errors = ErrorCheck(error_responses, message_error= message_error)

client.help_command = commands.MinimalHelpCommand()

@client.event
async def on_ready():
    game = discord.Game(playing)
    await client.change_presence(activity = game)
    print(f"logged in as: {client.user}\ndisplaying the status: {game}")

@client.event
async def on_guild_join(guild):
    print(f"Joined {guild.name}")

@client.event
async def on_command_error(ctx, error):
    await command_errors.check(messagable = ctx, author = ctx.author, error = error)

@client.command()
async def invite(ctx):
    embed = discord.Embed(title = f"{client.user.name}'s Invite", color = color, url = link)
    embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    await ctx.reply(embed = embed)

@client.command()
@perm_check()
async def status(ctx, *, status = None):
    if status:
        game = discord.Game(status)
        await client.change_presence(activity = game)
    else:
        await client.change_presence(activity = None)
    

@client.command()
@perm_check()
async def nick(ctx, guild : discord.Guild, *, bot_nick):
    await guild.me.edit(nick = bot_nick)

@client.command()
@perm_check()
async def reload(ctx):
    for file in os.listdir("./src/cogs"):
        if file.endswith(".py"):
            client.reload_extension(f"cogs.{file[:-3]}")
    await ctx.reply("reloaded cogs")

@client.event
async def on_message(message):
    # runs ctx commands
    await client.process_commands(message)

    if message.author == client.user or message.webhook_id:
        return

    connections = client.cogs["messaging"].connections

    # sends incoming messages
    if message.channel in connections.values():
        for pair in connections:
            if connections[pair] == message.channel:
                await pair.send(f"`{message.author.name}` {message.content}", allowed_mentions = discord.AllowedMentions.none())

            if message.attachments:
                for attachment in message.attachments:
                    file = await attachment.to_file()
                    await pair.send(file = file)

            for embed in message.embeds:
                await pair.send(embed = embed)

    # EVERYTHING PAST HERE IGNORES PREFIXES
    if message.content.startswith(client.command_prefix) or message.content.startswith(comment_prefix):
            return

    # sends outgoing messages
    if message.channel in connections.keys():
        if message.content:
            await connections[message.channel].send(content = message.content)

        if message.attachments:
            for attachment in message.attachments:
                file = await attachment.to_file()
                await connections[message.channel].send(file = file)

        for embed in message.embeds:
            await connections[message.channel].send(embed = embed)
        
    if message.channel.type == discord.ChannelType.private and message.channel not in (connections.keys() or connections.values()):
        print(f"{message.author.name}: {message.clean_content}")

@client.event
async def on_error(event, *args, **kwargs):
    await command_errors.message_error_reply(args[0])

client.run(token)
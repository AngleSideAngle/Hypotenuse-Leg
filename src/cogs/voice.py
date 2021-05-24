import discord
from discord.ext import commands
from utilities.permissions import perm_check
from discord.utils import get
from settings import color

class voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @perm_check()
    async def connect(self, ctx, channel_id):
        channel = await self.client.fetch_channel(channel_id)
        voice = get(self.client.voice_clients, guild=channel.guild)
        await channel.connect()
        await ctx.reply(f"connected to `{channel.name}`")
    
    @connect.error
    async def connect_error(self, ctx, error):
        msg = ""
        title = ""

        if isinstance(error, commands.CommandInvokeError):
            title = "Command Invoke Error"
            msg = "Enter a voice channel id that the bot has access to"
 
        if msg and title:
            embed = discord.Embed(title = title, color = color, description = msg)
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.reply(embed = embed)
        else:
            print(error)
    
    @commands.command()
    @perm_check()
    async def disconnect(self, ctx, guild : discord.Guild):
        await guild.voice_client.disconnect()
        await ctx.reply(f"disconnected in `{guild.name}`")


def setup(client):
    client.add_cog(voice(client))

# bad
'''
@client.command()
async def rick(ctx, server_id):
    if not await perm_check(ctx):
        return
    guild = await client.fetch_guild(server_id)
    voice = get(client.voice_clients, guild=guild)
    voice.play()
'''
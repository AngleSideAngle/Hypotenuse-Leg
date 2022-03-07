import discord
from discord.ext import commands
from utilities.functions import response
from discord.utils import get

class Voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx, channel_id : int):
        channel = await self.client.fetch_channel(channel_id)
        voice = get(self.client.voice_clients, guild=channel.guild)
        await channel.connect()
        await response(messageable = ctx, text = f"connected to `{channel.name}` in `{channel.guild.name}`")

    @commands.command()
    async def leave(self, ctx, guild : discord.Guild):
        await guild.voice_client.disconnect()
        await response(messageable = ctx, text = f"disconnected in `{guild.name}`")

def setup(client):
    client.add_cog(Voice(client))

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
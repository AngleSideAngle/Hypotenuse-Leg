import discord
from discord.ext import commands
from permissions import perm_check
from discord.utils import get

class voice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @perm_check()
    async def connect(self, ctx, channel : discord.VoiceChannel):
        voice = get(self.client.voice_clients, guild=channel.guild)
        await channel.connect()
        await ctx.send(f"connected to {channel.mention}")

    @commands.command()
    @perm_check()
    async def disconnect(self, ctx, guild : discord.Guild):
        await guild.voice_client.disconnect()
        await ctx.send(f"disconnected in {guild.name}")

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
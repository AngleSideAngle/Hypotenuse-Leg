from util import response

import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"logged in as: {self.client.user}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined {guild.name}")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await response(ctx, text=error, title="Error", color=discord.Colour.red())



def setup(client):
    client.add_cog(Events(client))

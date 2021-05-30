import discord
from discord.ext import commands
from settings import playing

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"logged in as: {self.client.user}")
    
    
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined {guild.name}")
    

def setup(client):
    client.add_cog(Events(client))
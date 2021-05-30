import discord
from discord.ext import commands
from utilities.functions import trusted
from secrets import link
from utilities.functions import response

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.id in trusted

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title = f"{self.client.user.name}'s Invite", color = ctx.me.color, url = link)
        await ctx.send(embed = embed)

    @commands.command()
    async def status(self, ctx, *, status = None):
        if status:
            game = discord.Game(status)
            await self.client.change_presence(activity = game)
        else:
            await self.client.change_presence(activity = None)
        await response(messageable = ctx, text = f"changed status to {game}")
        
    @commands.command()
    async def nick(self, ctx, guild : discord.Guild, *, nick):
        await guild.me.edit(nick = nick)
        await response(messageable = ctx, text = f"set bot nickname in `{guild.name}` to `{nick}`")

def setup(client):
    client.add_cog(Utility(client))
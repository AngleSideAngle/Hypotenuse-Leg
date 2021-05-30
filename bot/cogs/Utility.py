import discord
from discord.ext import commands
from utilities.functions import trusted
from secrets import link

import os

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.id in trusted

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title = f"{self.client.user.name}'s Invite", color = ctx.me.color, url = link)
        embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

    @commands.command()
    async def status(self, ctx, *, status = None):
        if status:
            game = discord.Game(status)
            await self.client.change_presence(activity = game)
        else:
            await self.client.change_presence(activity = None)

    @commands.command()
    async def nick(ctx, guild : discord.Guild, *, bot_nick):
        await guild.me.edit(nick = bot_nick)

def setup(client):
    client.add_cog(Utility(client))
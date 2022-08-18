from secret import link, trusted

import discord
from discord.ext import commands
from util import response


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return ctx.author.id in trusted

    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(
            title=f"{self.bot.user.name}'s Invite",
            color=ctx.me.color,
            url=link)
        await ctx.send(embed=embed)

    @commands.command()
    async def status(self, ctx, *, status=None):
        if status:
            game = discord.Game(status)
            await self.bot.change_presence(activity=game)
        else:
            await self.bot.change_presence(activity=None)
        await response(messageable=ctx, text=f"changed status to {game}")

    @commands.command()
    async def nick(self, ctx, guild: discord.Guild, *, nick):
        await guild.me.edit(nick=nick)
        await response(messageable=ctx, text=f"set bot nickname in `{guild.name}` to `{nick}`")


async def setup(bot):
    await bot.add_cog(Utility(bot))

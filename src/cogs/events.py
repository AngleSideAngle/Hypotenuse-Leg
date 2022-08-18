import discord
from discord.ext import commands
from util import response


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"logged in as: {self.bot.user}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"Joined {guild.name}")


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await response(ctx, text=error, title="Error", color=discord.Colour.red())

async def setup(bot):
    await bot.add_cog(Events(bot))

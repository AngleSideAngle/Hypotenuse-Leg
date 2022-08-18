import discord
from discord.ext import commands
from discord.utils import get
from util import response


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, channel_id: int):
        channel = await self.bot.fetch_channel(channel_id)
        voice = get(self.bot.voice_bots, guild=channel.guild)
        await channel.connect()
        await response(messageable=ctx, text=f"connected to `{channel.name}` in `{channel.guild.name}`")

    @commands.command()
    async def leave(self, ctx, guild: discord.Guild):
        await guild.voice_bot.disconnect()
        await response(messageable=ctx, text=f"disconnected in `{guild.name}`")


async def setup(bot):
    await bot.add_cog(Voice(bot))

# @bot.command()
# async def rick(ctx, server_id):
#     if not await perm_check(ctx):
#         return
#     guild = await bot.fetch_guild(server_id)
#     voice = get(bot.voice_bots, guild=guild)
#     voice.play()

import typing

import discord
from discord.ext import commands
from secret import trusted
from util import list_id


class Navigation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def cog_check(self, ctx):
        return ctx.author.id in trusted

    @commands.group(invoke_without_command=True)
    async def info(self, ctx: commands.Context):
        response = list_id(size=2048, data=[user async for user in self.bot.fetch_guilds()])
        for page in response:
            embed = discord.Embed(
                title=f"{self.bot.user.name}'s servers",
                color=ctx.me.color,
                description=f"`{self.bot.command_prefix}info channels <guild id>` for the channels of a guild\n`{self.bot.command_prefix}info members <guild id>` for the list of members in a guild\n`{self.bot.command_prefix}info member <member id>` for information about a member.{page}")

        await ctx.send(embed=embed)

    @info.command()
    async def channels(self, ctx, guild: discord.Guild):

        text = commands.Paginator(max_size=2048)
        voice = commands.Paginator(max_size=2048)
        for channel in await guild.fetch_channels():
            if channel.type == discord.ChannelType.text:
                text.add_line(f"{channel.name} • {channel.id}")
            elif channel.type == discord.ChannelType.voice:
                voice.add_line(f"{channel.name} • {channel.id}")

        for page in text.pages:
            embed = discord.Embed(
                title="Text",
                color=ctx.me.color,
                description=page)
            await ctx.send(embed=embed)

        for page in voice.pages:
            embed = discord.Embed(
                title="Voice",
                color=ctx.me.color,
                description=page)
            await ctx.send(embed=embed)

    @info.command()
    async def members(self, ctx, guild: discord.Guild):

        response = list_id(size=2048, data=[user async for user in guild.fetch_members()])

        for page in response:
            embed = discord.Embed(
                title=f"{guild.name} Members",
                color=ctx.me.color,
                description=page)
            await ctx.send(embed=embed)

    @info.command()
    async def member(self, ctx, user_id: int, guild: typing.Optional[discord.Guild] = None):

        if guild:
            user = guild.get_member(user_id)

            embed = discord.Embed(title=user, color=user.color)
            for activity in user.activities:
                if activity.type == discord.ActivityType.custom:
                    embed.description = activity.name
                else:
                    value = " "

                    if activity.type == discord.ActivityType.playing:
                        value = f"{activity.details}"
                    elif activity.type == discord.ActivityType.listening:
                        value = f"{activity.title}\nBy {activity.artist}"
                    elif activity.type == discord.ActivityType.streaming:
                        value = activity.game

                    embed.add_field(
                        name=activity.name,
                        value=f"```{value}```",
                        inline=False)

            for page in list_id(size=1024, data=user.roles):
                embed.add_field(name="Roles", value=page)

        else:
            user = self.bot.get_user(user_id)
            mutuals = list_id(size=1024, data=user.mutual_guilds)
            embed = discord.Embed(
                title=user,
                color=user.color,
                description="provide a guild that the user is in with `info member <user_id> <guild>` for more information")
            for page in mutuals:
                embed.add_field(name="mutual servers", value=page)

        embed.set_thumbnail(url=user.avatar)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Navigation(bot))

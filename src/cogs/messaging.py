import typing

import discord
from discord.ext import commands
from settings import comment_prefix, message_error
from util import inc_message, message_embed, perm_check, response


class Messaging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # open command group ----------------
    @commands.group(invoke_without_command=True)
    @perm_check()
    async def open(self, ctx):
        if not self.bot.connections:
            await response(messageable=ctx, text="there are no connections currently")
            return
        msg = commands.Paginator(max_size=2048)
        for connection in self.bot.connections:
            if connection.type == discord.ChannelType.text:
                line = f"{connection.guild.name}: {connection.name} • "
            else:
                line = f"DM {connection.recipient.name} • "

            if self.bot.connections[connection].type == discord.ChannelType.text:
                line += f"{self.bot.connections[connection].guild.name}: {self.bot.connections[connection].name}"
            else:
                line += f"DM {self.bot.connections[connection].recipient.name}"

            msg.add_line(line)

        for page in msg.pages:
            embed = discord.Embed(
                title="Active Channel Connections",
                color=ctx.me.color,
                description=page)
            await ctx.send(embed=embed)

    @open.command()
    @perm_check()
    async def close(self, ctx):
        if self.bot.connections[ctx.channel]:
            del self.bot.connections[ctx.channel]
            await response(messageable=ctx, text="channel reset")
        else:
            await response(messageable=ctx, text="there is no connection")

    @open.command()
    @perm_check()
    async def channel(self, ctx, channel_id: int):
        channel = await self.bot.fetch_channel(channel_id)

        if not channel.type == discord.ChannelType.text:
            raise commands.CommandInvokeError("The channel_id given must represent a text channel")
        self.bot.connections[ctx.channel] = channel
        await response(messageable=ctx, text=f"channel is `{self.bot.connections[ctx.channel]}`")

    @open.command()
    @perm_check()
    async def dm(self, ctx, user_id: int):
        user = self.bot.get_user(user_id)
        channel = await user.create_dm()

        self.bot.connections[ctx.channel] = channel
        await response(messageable=ctx, text=f"channel is `{self.bot.connections[ctx.channel]}`")

    @commands.command()
    async def reply(self, ctx, message_id: int, ping: typing.Optional[bool] = True, *, reply: str):

        channel = self.bot.connections[ctx.channel]
        message = channel.get_partial_message(message_id)
        sent_message = await message.reply(reply, allowed_mentions=discord.AllowedMentions(replied_user=ping))
        for embed in inc_message(message=sent_message):
            await ctx.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        connections = self.bot.connections

        # sends incoming messages
        if message.channel in connections.values():
            for pair in connections:
                if connections[pair] == message.channel:
                    for embed in inc_message(message=message):
                        await pair.send(embed=embed)

        # EVERYTHING PAST HERE IGNORES PREFIXES
        if message.content.startswith(self.bot.command_prefix) or message.content.startswith(comment_prefix):
            return

        # sends outgoing messages
        if message.channel in connections.keys():
            try:
                if message.content:
                    await connections[message.channel].send(content=message.content)

                if message.attachments:
                    for attachment in message.attachments:
                        file = await attachment.to_file()
                        await connections[message.channel].send(file=file)
            except discord.errors.Forbidden:
                await response(
                    messageable=message,
                    text=message_error[1],
                    title=message_error[0],
                    color=discord.Colour.red()
                )

        # prints dms to console
        if message.channel.type == discord.ChannelType.private and message.channel not in connections.keys() and message.channel not in connections.values():
            print(f"{message.author.name}: {message.clean_content}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        connections = self.bot.connections

        if before.content != after.content and after.channel in connections.values():
            for pair in connections:
                if connections[pair] == after.channel:
                    embed = message_embed(after)
                    embed.title = "Edit"
                    embed.add_field(name="Before", value=before.content[:1024])
                    embed.add_field(name="After", value=after.content[:1024])
                    await pair.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        connections = self.bot.connections

        if message.channel in connections.values():
            for pair in connections:
                if connections[pair] == message.channel:
                    for embed in inc_message(message=message):
                        embed.title = "Delete"
                        if embed.description and "~~" not in embed.description:
                            embed.description = f"~~{embed.description}~~"
                        await pair.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Messaging(bot))

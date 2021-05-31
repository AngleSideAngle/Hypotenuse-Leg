import discord
import typing
from discord.ext import commands
from secrets import trusted
from settings import comment_prefix
from utilities.functions import inc_message, incoming, response

class Messaging(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #makes all commands in this cog require trusted permissions
    async def cog_check(self, ctx):
        return ctx.author.id in trusted
    
    # open command group ----------------
    @commands.group(invoke_without_command = True)
    async def open(self, ctx):
        if not self.client.connections:
            await response(messageable = ctx, text = "there are no connections currently")
            return
        msg = commands.Paginator(max_size = 2048)
        for connection in self.client.connections:
            if connection.type == discord.ChannelType.text:
                line = f"{connection.guild.name}: {connection.name} • "
            else:
                line = f"DM {connection.recipient.name} • "

            if self.client.connections[connection].type == discord.ChannelType.text:
                line += f"{self.client.connections[connection].guild.name}: {self.client.connections[connection].name}"
            else:
                line += f"DM {self.client.connections[connection].recipient.name}"

            msg.add_line(line)

        for page in msg.pages:
            embed = discord.Embed(title = "Active Channel Connections", color = ctx.me.color, description = page)
            await ctx.send(embed = embed)
    
    @open.command()
    async def close(self, ctx):
        if self.client.connections[ctx.channel]:
            del self.client.connections[ctx.channel]
            await response(messageable = ctx, text = "channel reset")
        else:
            await response(messageable = ctx, text = "there is no connection")

    @open.command()
    async def channel(self, ctx, channel_id : int):
        channel = await self.client.fetch_channel(channel_id)
        
        if not channel.type == discord.ChannelType.text:
            raise commands.CommandInvokeError()
        self.client.connections[ctx.channel] = channel
        await response(messageable = ctx, text = f"channel is `{self.client.connections[ctx.channel]}`")

    @open.command()
    async def dm(self, ctx, user_id: int):
        user = self.client.get_user(user_id)
        channel = await user.create_dm()
        
        self.client.connections[ctx.channel] = channel
        await response(messageable = ctx, text = f"channel is `{self.client.connections[ctx.channel]}`")

    
    @commands.command()
    async def reply(self, ctx, message_id : int, ping : typing.Optional[bool] = True, *, reply : str):

        channel = self.client.connections[ctx.channel]
        message = await channel.fetch_message(message_id)
        await message.reply(reply, allowed_mentions = discord.AllowedMentions(replied_user = ping))

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.client.user:
            return

        connections = self.client.connections

        # sends incoming messages
        if message.channel in connections.values():
            for pair in connections:
                if connections[pair] == message.channel:
                    for embed in inc_message(message = message):
                        await pair.send(embed = embed)

        # EVERYTHING PAST HERE IGNORES PREFIXES
        if message.content.startswith(self.client.command_prefix) or message.content.startswith(comment_prefix):
                return

        # sends outgoing messages
        if message.channel in connections.keys():
            try:
                if message.content:
                    await connections[message.channel].send(content = message.content)

                if message.attachments:
                    for attachment in message.attachments:
                        file = await attachment.to_file()
                        await connections[message.channel].send(file = file)
            except discord.errors.Forbidden:
                await self.client.errors.message_error_reply(message)
            
        if message.channel.type == discord.ChannelType.private and message.channel not in connections.keys() and message.channel not in connections.values():
            print(f"{message.author.name}: {message.clean_content}")
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        connections = self.client.connections

        if before.content != after.content and after.channel in connections.values():
            for pair in connections:
                if connections[pair] == after.channel:
                    embed = incoming(after)
                    embed.title = "Edit"
                    embed.add_field(name = "Before", value = before.content[:1024])
                    embed.add_field(name = "After", value = after.content[:1024])
                    await pair.send(embed = embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        connections = self.client.connections
        
        if message.channel in connections.values():
            for pair in connections:
                if connections[pair] == message.channel:
                    for embed in inc_message(message = message):
                        embed.title = "Delete"
                        if embed.description and "~~" not in embed.description:
                            embed.description = f"~~{embed.description}~~"
                        await pair.send(embed = embed)
    
def setup(client):
    client.add_cog(Messaging(client))
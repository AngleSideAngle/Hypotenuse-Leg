import discord
import typing
from discord.ext import commands
from secrets import trusted
from settings import comment_prefix
from utilities.functions import list_id, incoming

class Messaging(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #makes all commands in this cog require trusted permissions
    async def cog_check(self, ctx):
        return ctx.author.id in trusted

    @commands.group(invoke_without_command = True)
    async def info(self, ctx):

        response = list_id(size = 2048, data = await self.client.fetch_guilds().flatten())
        for page in response:
            embed = discord.Embed(title = f"{self.client.user.name}'s servers", color = ctx.me.color, description = f"`{self.client.command_prefix}info channels <guild id>` for the channels of a guild\n`{self.client.command_prefix}info members <guild id>` for the list of members in a guild\n`{self.client.command_prefix}info member <member id>` for information about a member.{page}")

        await ctx.send(embed = embed)

    @info.command()
    async def channels(self, ctx, guild : discord.Guild):
        
        text = commands.Paginator(max_size = 2048)
        voice = commands.Paginator(max_size = 2048)
        for channel in await guild.fetch_channels():
            if channel.type == discord.ChannelType.text:
                text.add_line(f"{channel.name} • {channel.id}")
            elif channel.type == discord.ChannelType.voice:
                voice.add_line(f"{channel.name} • {channel.id}")
    
        for page in text.pages:
            embed = discord.Embed(title = "Text", color = ctx.me.color, description = page)
            await ctx.send(embed = embed)

        for page in voice.pages:
            embed = discord.Embed(title = "Voice", color = ctx.me.color, description = page)
            await ctx.send(embed = embed)

    @info.command()
    async def members(self, ctx, guild : discord.Guild):

        response = list_id(size = 2048, data = await guild.fetch_members().flatten())

        for page in response:
            embed = discord.Embed(title = f"{guild.name} Members", color = ctx.me.color, description = page)
            await ctx.send(embed = embed)

    @info.command()
    async def member(self, ctx, user_id : int, guild : typing.Optional[discord.Guild] = None):
        
        if guild:
            try:
                user = guild.get_member(user_id)
                
                embed = discord.Embed(title = user, color = user.color, description = f"{user.activities}\n{user.status}\n{user.roles}")
            except:
                await ctx.send("that user is not present in the server you specified")
                return
        else:
            user = self.client.get_user(user_id)
            mutuals = list_id(size = 1024, data = user.mutual_guilds)
            embed = discord.Embed(title = user, color = user.color, description = "provide a guild that the user is in with `info member <user_id> <guild>` for more information")
            for page in mutuals:
                embed.add_field(name = "mutual servers", value = page)

        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed = embed)
    
    # open command group ----------------
    @commands.group(invoke_without_command = True)
    async def open(self, ctx):
        if not self.client.connections:
            await ctx.send("there are no connections currently")
            return
        response = commands.Paginator(max_size = 2048)
        for connection in self.client.connections:
            if connection.type == discord.ChannelType.text:
                line = f"{connection.guild.name}: {connection.name} • "
            else:
                line = f"DM {connection.recipient.name} • "

            if self.client.connections[connection].type == discord.ChannelType.text:
                line += f"{self.client.connections[connection].guild.name}: {self.client.connections[connection].name}"
            else:
                line += f"DM {self.client.connections[connection].recipient.name}"

            response.add_line(line)

        for page in response.pages:
            embed = discord.Embed(title = "Active Channel Connections", color = ctx.me.color, description = page)
            await ctx.send(embed = embed)
    
    @open.command()
    async def close(self, ctx):
        if self.client.connections[ctx.channel]:
            del self.client.connections[ctx.channel]
            await ctx.send("channel reset")
        else:
            await ctx.send("there is no connection")

    @open.command()
    async def channel(self, ctx, channel_id : int):
        channel = await self.client.fetch_channel(channel_id)
        
        if not channel.type == discord.ChannelType.text:
            raise commands.CommandInvokeError()
        self.client.connections[ctx.channel] = channel
        await ctx.send(f"channel is `{self.client.connections[ctx.channel]}`")

    @open.command()
    async def dm(self, ctx, user_id: int):
        user = self.client.get_user(user_id)
        channel = await user.create_dm()
        
        self.client.connections[ctx.channel] = channel
        await ctx.send(f"channel is `{self.client.connections[ctx.channel]}`")

    
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
                    if message.content:
                        msg = incoming(message)
                        msg.description = message.clean_content

                        await pair.send(embed = msg)

                    for attachment in message.attachments:
                        if attachment.content_type == "image/png":
                            img = incoming(message)
                            img.set_image(url = attachment.url)
                            await pair.send(embed = img)
                        else:
                            file = await attachment.to_file()
                            await pair.send(file = file)

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
                    embed.add_field(name = "After", value = after.content[0:1024])
                    await pair.send(embed = embed)

def setup(client):
    client.add_cog(Messaging(client))
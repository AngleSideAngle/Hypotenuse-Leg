import discord
import typing
from discord.ext import commands
from secrets import trusted

class messaging(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.connections = {} # talking channel : receiving channel
    
    #makes all commands in this cog require trusted permissions
    async def cog_check(self, ctx):
        return ctx.author.id in trusted

    @commands.group(invoke_without_command = True)
    async def info(self, ctx):
        response = commands.Paginator(max_size = 2048)
        async for guild in self.client.fetch_guilds():
            response.add_line(f"{guild.name} • {guild.id}")
        for page in response.pages:
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
        response = commands.Paginator(max_size = 2048)
        for member in await guild.fetch_members().flatten():
            response.add_line(f"{member.name} • {member.id}")
        for page in response.pages:
            embed = discord.Embed(title = f"{guild.name} Members", color = ctx.me.color, description = page)
            await ctx.send(embed = embed)

    @info.command()
    async def member(self, ctx, member_id):
        await ctx.send("coming soon")
    
    @commands.group(invoke_without_command = True)
    async def open(self, ctx):
        del self.connections[ctx.channel]
        await ctx.send(f"channel reset")

    @open.command()
    async def channel(self, ctx, channel_id):
        channel = await self.client.fetch_channel(channel_id)
        
        if not channel.type == discord.ChannelType.text:
            raise commands.CommandInvokeError()
        self.connections[ctx.channel] = channel
        await ctx.send(f"channel is `{self.connections[ctx.channel]}`")

    @open.command()
    async def dm(self, ctx, user_id):
        user = await self.client.fetch_user(user_id)
        channel = await user.create_dm()
        
        self.connections[ctx.channel] = channel
        await ctx.send(f"channel is `{self.connections[ctx.channel]}`")

    @open.error
    async def open_error(self, ctx, error):
        msg = ""
        title = ""

        if isinstance(error, commands.CommandInvokeError) or isinstance(error, discord.NotFound):
            title = "Command Invoke Error"
            msg = "Enter a text channel id that the bot has access to"
 
        if msg and title:
            embed = discord.Embed(title = title, color = ctx.me.color, description = msg)
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
        else:
            print(error)
    

    @commands.command()
    async def active(self, ctx):
        if not self.connections:
            await ctx.send("there are no connections currently")
            return
        response = commands.Paginator(max_size = 2048)
        for connection in self.connections:
            if connection.type == discord.ChannelType.text:
                line = f"{connection.guild.name}: {connection.name} • "
            else:
                line = f"DM {connection.recipient.name} • "

            if self.connections[connection].type == discord.ChannelType.text:
                line += f"{self.connections[connection].guild.name}: {self.connections[connection].name}"
            else:
                line += f"DM {self.connections[connection].recipient.name}"

            response.add_line(line)
        for page in response.pages:
            embed = discord.Embed(title = "Active Channel Connections", color = ctx.me.color, description = page)
            await ctx.send(embed = embed)

    @commands.command()
    async def reply(self, ctx, message_id, ping : typing.Optional[bool] = True, *, reply):
        try:
            channel = self.connections[ctx.channel]
        except:
            print("e")
            return
        message = await channel.fetch_message(message_id)
        await message.reply(reply, allowed_mentions = discord.AllowedMentions(replied_user = ping))

def setup(client):
    client.add_cog(messaging(client))
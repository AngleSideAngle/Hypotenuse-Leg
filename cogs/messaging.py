import discord
import typing
from discord.ext import commands
from settings import color
from secrets import trusted

async def list_embed(ctx, list, title, left_name = "Names", right_name = "IDs"):
    names = [""]
    ids = [""]
    i = 0
    # guild.fetch_members()
    for member in list:
        if len(names[i] + member.name + ids[i] + str(member.id)) > 1023:
            names.append("")
            ids.append("")
            i += 1
        names[i] += f"{member.name}\n"
        ids[i] += f"{member.id}\n"
    

    response = discord.Embed(title =  title, color = color)
    response.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
    response.add_field(name = left_name, value = names[0])
    response.add_field(name = right_name, value = ids[0])
    await ctx.send(embed = response)
    for i in range(len(ids))[1:]:
        response = discord.Embed(color = color)
        response.add_field(name = left_name, value = names[i])
        response.add_field(name = right_name, value = ids[i])
        await ctx.send(embed = response)

class messaging(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.connections = {} # talking channel : receiving channel
    
    #makes all commands in this cog require trusted permissions
    async def cog_check(self, ctx):
        return ctx.author.id in trusted

    @commands.command()
    async def list(self, ctx, guild : typing.Optional[discord.Guild] = None):
        
        if guild: #lists all channels for server
            text_channels = []
            voice_channels = []
            for channel in await guild.fetch_channels():
                if channel.type == discord.ChannelType.text:
                    text_channels.append(channel)
                if channel.type == discord.ChannelType.voice:
                    voice_channels.append(channel)
            
            if text_channels:
                await list_embed(ctx, text_channels, title = guild.name, left_name = "Text")
            if voice_channels:
                await list_embed(ctx, voice_channels, title = guild.name, left_name = "Voice")
        else:
            servers = ""
            ids = ""
            async for guild in self.client.fetch_guilds():
                servers += f"{guild.name}\n"
                ids += f"{guild.id}\n"
            response = discord.Embed(title = f"{self.client.user.name}'s servers", color = color)
            response.add_field(name = "Names", value = servers)
            response.add_field(name = "IDs", value = ids)

            response.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = response)
            
        
    @commands.command()
    async def open(self, ctx, channel_id = None):
        if not channel_id:
            self.connections[ctx.channel] = None
            await ctx.send(f"channel reset")
            return

        channel = await self.client.fetch_channel(channel_id)
        
        if not channel.type == discord.ChannelType.text:
            raise commands.CommandInvokeError()
        self.connections[ctx.channel] = channel
        await ctx.send(f"channel is `{self.connections[ctx.channel]}`")

    @open.error
    async def open_error(self, ctx, error):
        msg = ""
        title = ""

        if isinstance(error, commands.CommandInvokeError):
            title = "Command Invoke Error"
            msg = "Enter a text channel id that the bot has access to"
 
        if msg and title:
            embed = discord.Embed(title = title, color = color, description = msg)
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.send(embed = embed)
        else:
            print(error)

    @commands.command()
    async def members(self, ctx, guild : discord.Guild):
        await list_embed(ctx, list = await guild.fetch_members().flatten(), title = f"{guild.name} members")

    @commands.command()
    async def active(self, ctx):
        if not self.connections:
            await ctx.send("there are no connections currently")
            return

        sending = ""
        receiving = ""
        for connection in self.connections:
            if self.connections[connection]:    
                if connection.type == discord.ChannelType.text:
                    sending += f"**{connection.guild.name}** {connection.name}\n"
                elif connection.type == discord.ChannelType.private:
                    sending += f"**DM** {connection.recipient.name}\n"

                if self.connections[connection].type == discord.ChannelType.text:
                    receiving += f"**{self.connections[connection].guild.name}** {self.connections[connection].name}\n"
                elif self.connections[connection].type == discord.ChannelType.private:
                    receiving += f"**DM** {self.connections[connection].recipient.name}\n"

        response = discord.Embed(title = "Open Connections", color = color)
        response.add_field(name = "sending", value = sending)
        response.add_field(name = "receiving", value = receiving)
        await ctx.send(embed = response)

def setup(client):
    client.add_cog(messaging(client))
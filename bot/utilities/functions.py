import discord
from discord.ext import commands
from secrets import trusted

def list_id(size : int, data : tuple, seperator : str = " • ") -> tuple:
    '''
    Creates and runs a discord.commands Paginator through a list of data.
    Returns a list of strings that look like this:
    ```
    name of item • id of item
    name of item 2 • id of item 2
    etc
    ```
    '''
    book = commands.Paginator(max_size = size)

    if len(data) == 0:
        return

    for item in data:
        line = seperator.join((item.name, str(item.id)))
        book.add_line(line)

    return book.pages

def perm_check():
    '''
    Allows this to be used as a decorator like:
    @perm_check
    '''
    async def predicate(ctx):
        '''
        Limits access to a command to only users in trusted
        '''
        return ctx.author.id in trusted
    return commands.check(predicate)
    
async def response(messageable : discord.abc.Messageable, text : str, title : str = None, color : discord.Colour = None):
    '''
    Generates and sends a simple discord Embed as a reply to the messageable
    '''
    msg = discord.Embed(description = text)
    if title:
        msg.title = title
    if color:
        msg.color = color
    else:
        if isinstance(messageable, commands.Context):
            msg.color = messageable.me.color
        else:
            msg.color = messageable.guild.me.color
    await messageable.reply(embed = msg, mention_author = False)
    
def incoming(message : discord.Message) -> discord.Embed:
    '''
    Returns a discord Embed giving information about a message.
    Used to show messages from one channel in another
    '''
    
    embed = discord.Embed(color = message.author.color)
    embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
    embed.set_footer(text = f"{message.author} • {message.author.id}\n{message.channel} • {message.id}")
    return embed

def inc_message(message : discord.Message) -> list:
    result = []
    if message.content:
        msg = incoming(message = message)
        msg.description = message.clean_content
        result.append(msg)

    for attachment in message.attachments:
        if "image" in attachment.content_type:
            img = incoming(message = message)
            img.set_image(url = attachment.url)
            result.append(img)
    
    for embed in message.embeds:
        result.append(embed)

    return result
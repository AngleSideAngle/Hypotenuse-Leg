from secrets import trusted

import discord
from discord.ext import commands

from settings import repo


class EmbedHelp(commands.MinimalHelpCommand):

    async def send_bot_help(self, mapping):
        help = discord.Embed(
            title="Help",
            color=self.context.me.color,
            description="`+help command/category/group` for more info on commands.")
        for cog in mapping:
            if cog:
                name = cog.qualified_name
            else:
                name = "Other"

            book = commands.Paginator(max_size=1024)
            for command in mapping[cog]:
                book.add_line(command.name)

            for page in book.pages:
                help.add_field(
                    name=name,
                    value=page
                )

        developer = await self.context.bot.fetch_user(547910268081143830)
        help.set_footer(text=repo, icon_url=developer.avatar_url)

        await self.get_destination().send(embed=help)

    async def send_cog_help(self, cog):
        book = commands.Paginator()

        for command in cog.get_commands():
            book.add_line(command.name)

        for page in book.pages:
            help = discord.Embed(title=cog.qualified_name,
                                 color=self.context.me.color, description=page)
            await self.get_destination().send(embed=help)


def list_id(size: int, data: tuple, seperator: str = " • ") -> tuple:
    '''
    Creates and runs a discord.commands Paginator through a list of data.
    Returns a list of strings that look like this:
    ```
    name of item • id of item
    name of item 2 • id of item 2
    etc
    ```
    '''
    book = commands.Paginator(max_size=size)

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


async def response(messageable: discord.abc.Messageable, text: str, title: str = None, color: discord.Colour = None):
    '''
    Generates and sends a simple discord Embed as a reply to the messageable
    '''
    msg = discord.Embed(description=text)
    if title:
        msg.title = title
    if color:
        msg.color = color
    else:
        if isinstance(messageable, commands.Context):
            msg.color = messageable.me.color
        else:
            msg.color = messageable.guild.me.color
    await messageable.reply(embed=msg, mention_author=False)


def message_embed(message: discord.Message) -> discord.Embed:
    '''
    Returns a discord Embed giving information about a message.
    Used to show messages from one channel in another
    '''

    embed = discord.Embed(color=message.author.color)
    embed.set_author(name=message.author.display_name,
                     icon_url=message.author.avatar_url)
    embed.set_footer(
        text=f"{message.author} • {message.author.id}\n{message.channel} • {message.id}")
    return embed


def inc_message(message: discord.Message) -> list:
    '''
    Returns a list of embeds that make up an incoming message
    '''
    result = []
    if message.content:
        msg = message_embed(message=message)
        msg.description = message.clean_content
        result.append(msg)

    for attachment in message.attachments:
        if "image" in attachment.content_type:
            img = message_embed(message=message)
            img.set_image(url=attachment.url)
            result.append(img)

    for embed in message.embeds:
        result.append(embed)

    return result

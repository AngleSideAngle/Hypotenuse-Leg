from discord.ext import commands
from secrets import trusted

def perm_check():
    async def predicate(ctx):
        return ctx.author.id in trusted
    return commands.check(predicate)
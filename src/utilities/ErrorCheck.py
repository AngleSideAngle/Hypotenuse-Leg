import discord

class ErrorCheck:
    def __init__(self, responses : dict):
        self.responses = responses

    async def check(self, ctx, error):
        title = None
        msg = None
        for i in self.responses:
            if isinstance(error, i):
                title = self.responses[i][0]
                msg = self.responses[i][1]
        if msg and title:
            embed = discord.Embed(title = title, color = ctx.author.color, description = msg)
            embed.set_author(name = ctx.author, icon_url = ctx.author.avatar_url)
            await ctx.reply(embed = embed)
        else:
            print(error)
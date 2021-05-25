import discord

class ErrorCheck:
    def __init__(self, responses : dict, message_error : tuple):
        self.responses = responses
        self.message_error = message_error

    async def check(self, messagable, author, error):
        title = None
        msg = None
        for i in self.responses:
            if isinstance(error, i):
                title = self.responses[i][0]
                msg = self.responses[i][1]
        if msg and title:
            embed = discord.Embed(title = title, description = msg, color = discord.Colour.dark_theme())
            await messagable.reply(embed = embed)
        else:
            print(error)

    async def message_error_reply(self, message):
        embed = discord.Embed(title = self.message_error[0], description = self.message_error[1], color = discord.Colour.dark_theme())
        await message.reply(embed = embed)
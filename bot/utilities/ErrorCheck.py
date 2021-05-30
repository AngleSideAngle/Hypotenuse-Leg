import discord
from utilities.functions import response

class ErrorCheck:
    def __init__(self, responses : dict, message_error : tuple):
        self.responses = responses
        self.message_error = message_error

    async def check(self, messageable, error):
        title = None
        msg = None
        for i in self.responses:
            if isinstance(error, i):
                title = self.responses[i][0]
                msg = self.responses[i][1]
        if msg and title:
            await response(messageable = messageable, text = msg, title = title, color = discord.Colour.red())
        else:
            print(error)

    async def message_error_reply(self, message : discord.Message):
        await response(messageable = message, text = self.message_error[1], title = self.message_error[0], color = discord.Colour.red())
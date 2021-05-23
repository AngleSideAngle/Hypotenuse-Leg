import discord
from discord.ext import commands
from discord.ext.commands.errors import BotMissingAnyRole, BotMissingPermissions, CheckFailure
playing = "The Legend of Zelda: Breath of the Wild"
color = discord.Colour.blue()
command_prefix = '+'
comment_prefix = '#'

error_responses = {
    commands.errors.CommandNotFound : (
        "Command Not Found",
        "The command you tried does not exist"
    ),
    commands.errors.BotMissingPermissions : (
        "Missing Permissions",
        f"The bot lacks required permissions"
    ),
    commands.errors.MissingRequiredArgument : (
        "Missing Required Arguments",
        "You did not input the command's arguments correctly, refer to `help` for information on how to use the command"
    ),
    commands.errors.CheckFailure : (
        "Check Failure",
        "You do not have the required permissions to run this command"
    )
}
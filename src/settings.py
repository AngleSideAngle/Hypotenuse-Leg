import discord
from discord.ext import commands
playing = "The Legend of Zelda: Breath of the Wild" # this currently doesn't do anything
repo = "https://github.com/AngleSideAngle/Half-Life" # please do not change this
command_prefix = '+'
comment_prefix = '#'

error_responses = {
    commands.errors.CommandNotFound : (
        "Command Not Found",
        "The command you tried does not exist"
    ),
    commands.errors.BotMissingPermissions : (
        "Missing Permissions",
        "The bot lacks required permissions"
    ),
    commands.errors.MissingRequiredArgument : (
        "Missing Required Arguments",
        "You did not input the command's arguments correctly, refer to `help` for information on how to use the command"
    ),
    commands.errors.CheckFailure : (
        "Check Failure",
        "You do not have the required permissions to run this command"
    ),
    commands.errors.CommandInvokeError : (
        "Invoke Error",
        "The command encountered an error, check to see if the arguments you gave are correct and the bot has access to them"
    ),
    commands.errors.BadArgument : (
        "Bad Argument",
        "You did not input the command's arguments correctly, refer to `help` for information on how to use the command"
    )
}

message_error = (
    "Missing Permissions",
    "The bot lacks required permissions"
)
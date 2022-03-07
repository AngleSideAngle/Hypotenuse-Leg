import discord
from discord.ext import commands
from settings import repo

class EmbedHelp(commands.MinimalHelpCommand):
    
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        help = discord.Embed(
            title = "Help", 
            color = self.context.me.color, 
            description = f"`+help command/category/group` for more info on commands."
        )
        for cog in mapping:
            if cog:
                name = cog.qualified_name
            else:
                name = "Other"
            
            book = commands.Paginator(max_size = 1024)
            for command in mapping[cog]:
                book.add_line(command.name)
            
            for page in book.pages:
                help.add_field(
                    name = name,
                    value = page
                )

        developer = await self.context.bot.fetch_user(547910268081143830)
        help.set_footer(text = repo, icon_url = developer.avatar.url)
            
        await self.get_destination().send(embed = help)

    async def send_cog_help(self, cog):
        book = commands.Paginator()

        for command in cog.get_commands():
            book.add_line(command.name)
        
        for page in book.pages:
            help = discord.Embed(title = cog.qualified_name, color = self.context.me.color, description = page)
            await self.get_destination().send(embed = help)

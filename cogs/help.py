import disnake
from disnake.ext import commands, tasks
from env import *

class Help(commands.Cog):


    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Help is geladen!")
 

    # Commands
    @commands.slash_command(description="Laat het help menu zien")
    async def help(self, inter):
        guild = self.bot.get_guild(Env.GUILD_ID)
        embed = disnake.Embed(title="Help menu", description="Vrienden voor altijd! - Commands", color=0x4793FF)
        embed = embed.add_field(name="/voice versleep", value="Hiermee versleep je een gebruiken naar een ander voice kanaal", inline=False)

        await inter.response.send_message(embed=embed, ephemeral=True)


        
def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
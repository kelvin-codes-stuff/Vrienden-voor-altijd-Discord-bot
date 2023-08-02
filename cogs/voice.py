import disnake
from disnake.ext import commands, tasks
from env import *

class Voice(commands.Cog):


    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Voice is geladen!")


    # Commands
    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command()
    async def voice(self, inter):
        pass


    @voice.sub_command(description="versleep een lid naar een ander voice kanaal")
    async def versleep(self, inter, gebruiker: disnake.Member, kanaal=commands.Param(choices={"Lounge": "lounge", "Bezig": "bezig", "AFK": "afk"})):
        # Checks if user in VC, otherwise show error to user
        if gebruiker.voice == None:
            await inter.response.send_message("Je kunt niet iemand verplaatsen die niet in een voicechat zit!", ephemeral=True)
            return 
        
        if kanaal == "lounge":
            channel = self.bot.get_channel(Env.VC_LOUNGE_ID)
        elif kanaal == "bezig":
            channel = self.bot.get_channel(Env.VC_BEZIG_ID)
        elif kanaal == "afk":
            channel = self.bot.get_channel(Env.VC_AFK_ID)

        await gebruiker.edit(voice_channel=channel)

        await inter.response.send_message(f"Gebruiker `{gebruiker.name}` is naar `{channel.name}` verplaatst", ephemeral=True)

        
def setup(bot: commands.Bot):
    bot.add_cog(Voice(bot))
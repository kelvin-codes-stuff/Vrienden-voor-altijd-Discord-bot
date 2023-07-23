import disnake
from disnake.ext import commands, tasks
from env import *

class Other(commands.Cog):


    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Other is geladen!")
 

    # Invite command
    @commands.slash_command(description="Maak een invite link aan")
    async def invite(self, inter):
        channel = self.bot.get_channel(Env.ALGEMEEN_ID)
        invite = await channel.create_invite(max_age=0, max_uses=0, temporary=False)
        await inter.response.send_message(f"**Invite link:** {invite}", ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Other(bot))
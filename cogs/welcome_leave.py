import disnake
from disnake.ext import commands, tasks
from env import *
from datetime import datetime

class Welcome_leave(commands.Cog):


    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("Cog Welcome_leave is geladen!")


    # Listeners
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await Welcome_leave.member_join_embed(self, member)
        print(f"{member.name} is gejoined!")


    # Functions
    async def member_join_embed(self, member):
        
        hour_now = int(datetime.now().strftime("%H"))
        channel_to_send = self.bot.get_channel(Env.ALGEMEEN_ID)

        if hour_now >= 6 and hour_now < 12:
            time_set = "Goedemorgen"
        elif hour_now >= 12 and hour_now < 18:
            time_set = "Goedemiddag"
        elif hour_now >= 18 and hour_now < 24:
            time_set = "Goedeavond"
        else:
            time_set = "Goedenacht"

        embed = disnake.Embed(title="Er is een nieuw lid erbij gekomen!", description=f"{time_set} {member.mention}, welkom op onze server! We hopen dat je het naar je zin zal gaan hebben!", color=disnake.Color.blue())
        embed.set_author(name=member.name, icon_url=member.avatar)
        await channel_to_send.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Welcome_leave(bot))
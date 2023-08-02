import disnake
from disnake.ext import commands
from env import *

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.listening , name="jou"))
    print("De bot is ready to rock!")


bot.load_extension("cogs.voice")
bot.load_extension("cogs.help")
bot.load_extension("cogs.welcome_leave")
bot.load_extension("cogs.other")
bot.load_extension("cogs.birthday")


if __name__ == "__main__":
    bot.run(Env.TOKEN)
    
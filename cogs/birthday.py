import disnake
from disnake.ext import commands, tasks
from disnake.enums import ButtonStyle
from env import *
from database import Database
from datetime import datetime
import pytz

# TODO change month string to int

class birthday(commands.Cog):

    
    def __init__(self, bot: commands.Bot):



        self.bot = bot
        print("Cog Birthday is loaded!")



        # Main birthday command
        @bot.slash_command()
        async def verjaardag(inter):
            pass


        
        # Adding birthday command
        @verjaardag.sub_command(description = "Voeg je verjaardag toe aan deze bot!")
        @commands.cooldown(1, 10.0, commands.BucketType.member)
        async def toevoegen(
            # Defining slash values
            inter: disnake.ApplicationCommandInteraction,
            day: int = commands.Param(le=31, name="dag"),
            month = commands.Param(name="maand", choices= {"Januari": "01", "Februari": "02", "Maart": "03", "April": "04", "Mei": "05", "Juni": "06", "Juli": "07", "Augustus": "08", "September": "09", "Oktober": "10", "November": "11", "December": "12"}),
            year: int = commands.Param(name="jaar", le=2023),
            ):
            
            if len(str(day)) < 2:
                day = "0" + str(day)

            if len(str(year)) < 4:
                await inter.response.send_message("Je moet het jaartal invullen met een lengte van 4 zoals: '2001'.", ephemeral=True)
                
            else:
                # Execute stuff to database
                resp = birthday_add(inter, day, month, year)
                
                # Send the right response back, based on what 'birthday_add' gives as response back
                if resp == 1:
                    await inter.response.send_message(f"Je hebt de volgende verjaardag ingesteld: {day}-{month}-{year}. Mocht dit niet juist zijn voer dan dit command opnieuw uit na de countdown van 10 seconden", ephemeral=True)
                elif resp == 2:
                    await inter.response.send_message(f"Je hebt je verjaardag gewijzigd naar: {day}-{month}-{year}. Mocht dit niet juist zijn voer dan dit command opnieuw uit na de countdown van 10 seconden", ephemeral=True)
                elif resp == 0:
                    await inter.response.send_message(f"Oepsiedoepsie, er ging wat mis!", ephemeral=True)



        # Removing birthday command
        @commands.cooldown(1, 10.0, commands.BucketType.member)
        @verjaardag.sub_command(description="Verwijder je verjaardag uit Adje!")
        async def verwijderen(inter):
            
            if birthday_remove(id=inter.author.id) != False:
                await inter.response.send_message(f"Ik heb je verjaardag verwijderd uit de database!", ephemeral=True)
            else:
                await inter.response.send_message(f"Ik kon geen verjaardag vinden helaas!", ephemeral=True)
            

            
        # Cooldown message
        @verjaardag.error
        @verwijderen.error
        async def test_error(inter: disnake.GuildCommandInteraction, error: Exception) -> None:
            if isinstance(error, commands.CommandOnCooldown):
                new_error = str(error).split(" ")[7]
                return await inter.response.send_message(
                    f"Dit command heeft een cooldown, probeer het over `{new_error}` opnieuw.", ephemeral=True
                )

        

        # Functions
        def birthday_add(inter, day, month, year):
            # F
            try:
                Database.cursor.execute(f"Select * FROM birthday_users WHERE user_id='{inter.author.id}'")
                res = Database.cursor.fetchone()

                day_formatted = str(day) + "-" + str(month).lower()

                if res == [] or res == None:
                    Database.cursor.execute(f"INSERT INTO birthday_users (user_id, birthday, year) VALUES ('{int(inter.author.id)}', '{str(day_formatted)}', '{year}')")
                    Database.db.commit()
                    return 1
                else:
                    Database.cursor.execute(f"UPDATE birthday_users SET birthday = '{str(day_formatted)}', year = '{year}' WHERE user_id='{inter.author.id}'")
                    Database.db.commit()
                    return 2
                
            except Exception as error:
                print(f"DEBUG birthday funtion 'birthday_add', error: {error}")
        


        def birthday_remove(id):
            try:
                Database.cursor.execute(f"SELECT * FROM birthday_users WHERE user_id = {id}")
                if Database.cursor.fetchone() == None or Database.cursor.fetchone() == []:
                    return False
                else:
                    Database.cursor.execute(f"DELETE FROM birthday_users WHERE user_id = {id}")
                    Database.db.commit()

            except Exception as error:
                print(f"DEBUG birthday funtion 'birthday_remove', error: {error}")



        async def birthday_send_embed(id, age):
            try:
                channel_to_send = bot.get_channel(Env.ALGEMEEN_ID)
                user = (await bot.get_or_fetch_user(int(id))).mention
                user_avatar = (await bot.get_or_fetch_user(int(id))).avatar

                embed=disnake.Embed(title=f"Iemand is {age} geworden!", description=f"**{user}, gefeliciteerd met je verjaardag!**", color=0xdf8cfe)
                embed.set_thumbnail(url=user_avatar)

                bot.loop.create_task(channel_to_send.send(embed=embed, allowed_mentions=disnake.AllowedMentions.all()))
                
            except Exception as error:
                print(error)
                pass



        # Birthday loop to check date
        bd_counter = [0] 
        @tasks.loop(seconds=10) 
        async def birthday_date_checkert():

            datetime_AM = datetime.now(pytz.timezone('Europe/Amsterdam') )
            now_time = datetime_AM.strftime("%H%M")
            now_date = datetime_AM.strftime("%d-%m")

            if now_time == "1030" and bd_counter[0] < 1:
                bd_counter[0] = 1

                try:
                    Database.cursor.execute("SELECT * FROM birthday_users")               
                    res = Database.cursor.fetchall()

                    for birthday_user in res:

                        if birthday_user[2] == now_date:
                            calculate_age = int(datetime_AM.strftime("%Y")) - int(birthday_user[3])
                            print(f"Jeeej for user: {birthday_user[1]}, hij is {calculate_age} geworden!")
                            
                            await birthday_send_embed(id=birthday_user[1], age=calculate_age)
            
                except Exception as error:
                    print(f"DEBUG birthday funtion, Error= {error}")

            if now_time == "1031":
                bd_counter[0] = 0
            
        birthday_date_checkert.start()





def setup(bot: commands.Bot):
    bot.add_cog(birthday(bot))                    
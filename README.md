## Vrienden voor Altijd Discord bot
Gemaakt door @kelvin-codes-stuff


## Functies

**Publiekelijk**
- `/help` - Laat een help menu zien

**Beheer**
- `/voice verplaats <gebruiker> <kanaal>`



## Setup
- git clone https://github.com/kelvin-codes-stuff/Vrienden-voor-altijd-Discord-bot
- cd Vrienden-voor-altijd-Discord-bot
- mv env.example.py env.py
- nano env.example.py
- docker build -t discord_bot .
- docker run -d --name discord-bot discord_bot:latest
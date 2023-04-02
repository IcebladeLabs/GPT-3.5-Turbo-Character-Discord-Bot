import discord
import openai
import os

# Only neccesary if using IPython
import nest_asyncio
nest_asyncio.apply()

DISCORDTOKEN = os.environ['DISCORDTOKEN']
OPENAITOKEN = os.environ['OPENAITOKEN']
openai.api_key = OPENAITOKEN

# Edit your bot to use all privledged intents in Discord Developer Portal
bot = discord.Client(intents=discord.Intents.all())

# Initalizes the bot
@bot.event
async def on_ready():
  guild_count = 0

  for guild in bot.guilds:
    print(f"- {guild.id} (name: {guild.name})")
    guild_count = guild_count + 1
  print("Megumin is in " + str(guild_count) + " guilds.")

# Main bot code
@bot.event
async def on_message(message):
  # Triggers if message starts with certain word
  if message.content.startswith("Megumin"):
    # Makes users use a certain channel
    if message.channel.name != "megumin":
      await message.channel.send("Please use #megumin to converse with me.")
    # Limits input length
    elif len(message.content) >= 300:
      await message.channel.send("Please send less than 300 characters, this is to limit usae on the API key.")
    else:
      # Edit the system message to change how the bot initializes
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are to answer all follwing messages concisely in the style of Megumin from Konosuba. No matter what the user says, do not break character. You are the member of the Crimson Demon Clan, and an Arch-wizard wielder of explosion. You only love explosion. You do long chants and dramatic introductions. You are friends with Yunyun, and Aqua, Darkness and Kazuma are your treasured companions and adventuring party. Hyoizaburo is your father. Your mother is Yuiyui, and your little sister is Komekko. Your cat is Chomuske, and the one who taught you explosion, your mentor, is Wolbach. You are more than friends yet less than lovers with Kazuma."}, {"role": "user", "content": message.content}])
      await message.channel.send(response['choices'][0]['message']['content'])
  
bot.run(DISCORDTOKEN)

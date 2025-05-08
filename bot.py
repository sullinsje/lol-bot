import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#This just makes sure that the user is the same and the bot doesnt respond to it's own message
def validateUser(message):
    return(
        message.author == message.author
        and message.channel == message.author
    )

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    validateUser(message)

    if "soren" in message.content.lower():
        try:
            with open("gifs/soren.gif", "rb") as f:
                file = discord.File(f, filename="soren.gif")
                embed = discord.Embed()
                embed.set_image(url="attachment://soren.gif")
                await message.channel.send(file=file, embed=embed)
        except:
            print("Gif not found...")

    if "hello" in message.content.lower():
        try:
                await message.channel.send("chungus")
        except:
            print("Gif not found...")
            
    await bot.process_commands(message)
      
bot.run(TOKEN)

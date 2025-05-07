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

@bot.command(name="lol")
async def hello(ctx):
    await ctx.send("lol")

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
# @bot.command(name="employees")
# async def employees(ctx):
#     try:
#         response = requests.get("http://localhost:8000/employees/")
#         response.raise_for_status()
#         employees = response.json()

#         if not employees:
#             await ctx.send("No employees found")
#         else:
#             names = [emp.get("name", "Unknown") for emp in employees]
#             reply = "Employees:\n" + "\n".join(f"- {name}" for name in names)
#             await ctx.send(reply)
          
#     except requests.RequestException as e:
#             await ctx.send(f"Failed to get employee(s):\n{e}")
      
bot.run(TOKEN)

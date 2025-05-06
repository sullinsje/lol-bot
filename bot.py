import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#This just makes sure that the user is the same and the bot doesnt respond to it's own message
def validateUser(message):
    return(
        message.author == ctx.author
        and message.channel == ctx.author
    )

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello")

@bot.command(name="employees")
async def employees(ctx):
    try:
        response = requests.get("http://localhost:8000/employees/")
        response.raise_for_status()
        employees = response.json()

        if not employees:
            await ctx.send("No employees found")
        else:
            names = [emp.get("name", "Unknown") for emp in employees]
            reply = "Employees:\n" + "\n".join(f"- {name}" for name in names)
            await ctx.send(reply)
          
    except requests.RequestException as e:
            await ctx.send(f"Failed to get employee(s):\n{e}")
      
TOKEN = ''
bot.run(TOKEN)

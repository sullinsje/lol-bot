import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

#This just makes sure that the user is the same and the bot doesnt respond to it's own message
def isBot(message):
    if message.author == bot.user:
        return True

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command("gifs")
async def gifs(ctx):
    csv_file = "links.csv"

    df = pd.read_csv(csv_file)

    names = df['Name']
    message = ""

    for name in names:
        message += f"- {name}\n"

    await ctx.send(message)
    

@bot.command("upload")
async def upload_gif(ctx, *, gif_link: str):
    try:
        gif, name = gif_link.rsplit(" ", 1)
    except ValueError:
        await ctx.send("smth messed up...")
        
    try: 
        csv_file = "links.csv"

        df = pd.read_csv(csv_file)

        existing_index = df.index[df['Name'].str.lower() == name.lower()]

        if not existing_index.empty:
            df.loc[existing_index, 'Gif'] = gif
            await ctx.send(f"Updated GIF for name: `{name}`")
        else:
            new_row = {'Name': name, 'Gif': gif}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            await ctx.send(f"Added new GIF with name: `{name}`")

        df.to_csv(csv_file, index=False, mode='w')
        return
    except:
        await ctx.send("smth messed up...")


@bot.event
async def on_message(message):
    if isBot(message):
        return

    csv_file = "links.csv"
    df = pd.read_csv(csv_file)

    names = df['Name']
    
    for name in names:
        if name in message.content.lower():
            try:
                gif = df['Gif'][df['Name'] == name]
                await message.channel.send(gif.values[0])
            except:
                print("smth messed up...")
            
    await bot.process_commands(message)
      
bot.run(TOKEN)


            # with open("gifs/soren.gif", "rb") as f:
            #     file = discord.File(f, filename="soren.gif")
            #     embed = discord.Embed()
            #     embed.set_image(url="attachment://soren.gif")
            #     await message.channel.send(file=file, embed=embed)
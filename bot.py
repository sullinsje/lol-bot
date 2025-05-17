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

#region
words = ['nigga', 'nigger']
#endregion

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

async def send_gif(message):
    links = "links.csv"
    df = pd.read_csv(links)

    names = df['Name']
    
    for name in names:
        if name in message.content.lower():
            try:
                gif = df['Gif'][df['Name'] == name]
                await message.channel.send(gif.values[0])
            except:
                print("smth messed up...")

async def get_stats(message):
    for x in words:
        if x in message.content.lower():
            stats = "stats.csv"
            df = pd.read_csv(stats)
            user = message.author.name

            existing_index = df.index[df['User'].str.lower() == user.lower()]

            if not existing_index.empty:
                df.loc[df['User'].str.lower() == user.lower(), 'Amount'] += 1
                amount = df.loc[df['User'].str.lower() == user.lower(), 'Amount'].values[0]

                message_to_send = f"{user} has said the N word {amount} times"
                await message.channel.send(message_to_send)

            else:
                new_row = {'User': user, 'Amount': 1}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                await message.channel.send(f"{user} has said the N word for the first time in `{message.channel}`")

            df.to_csv(stats, index=False, mode='w')
            return
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
        gif, name = gif_link.split(" ", 1)
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

@bot.command("delete")
async def delete_gif(ctx, *, name: str):
        
    try: 
        csv_file = "links.csv"

        df = pd.read_csv(csv_file)

        existing_index = df.index[df['Name'].str.lower() == name.lower()]

        if not existing_index.empty:
            df = df.drop(existing_index)
            await ctx.send(f"Deleted GIF for name: `{name}`")

        df.to_csv(csv_file, index=False, mode='w')
        return
    except:
        await ctx.send("smth messed up...")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await send_gif(message)
    await get_stats(message)      

    await bot.process_commands(message)
      
bot.run(TOKEN)

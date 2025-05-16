import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

@bot.event
async def on_ready():
     await bot.sync_commands()

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

@bot.event
async def on_ready():
    print(f'Nyxx is online and ready to go!')
    change_status.start()
    
@tasks.loop(seconds=10)  # Change status every 10 seconds
async def change_status():
    await bot.wait_until_ready()  # Ensure the bot is ready
    while True:
        server_count = len(bot.guilds)
        statuses = [
            discord.Game(name="Now Online via Visual Studio Code"),
            discord.Game(name="Helping people with Homebrew issues"),
            discord.Game(name=f"Watching {server_count} servers!"),
            discord.Game(name="discord.gg/QQXVaFbD4K"),
            discord.Game(name="youtube.com/@fwdrxyy_"),
            discord.Game(name="New Feature! ModMail System"),
        ]
        for status in statuses:
            await bot.change_presence(activity=status, status=discord.Status.online)
            await asyncio.sleep(10)

@bot.event
async def on_ready():
    if not change_status.is_running():
        change_status.start()
  

     
# Load cogs (modules)
bot.load_extension('Cogs.Moderation')
bot.load_extension('Cogs.General')
bot.load_extension('Cogs.Homebrews')
bot.load_extension('Cogs.Pretendo')
bot.load_extension('Cogs.AutoFeatures')
bot.load_extension('Cogs.ReactionRoles')
bot.load_extension('Cogs.ModMail')
bot.load_extension('Cogs.Logging')
bot.load_extension('Cogs.ServerManagement')

bot.run(TOKEN)
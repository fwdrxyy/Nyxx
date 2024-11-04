import discord
from discord.ext import commands, tasks
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

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
            discord.Game(name="Now Online 24/7 thanks to Dires!"),
            discord.Game(name="Rewritten codebase"),
            discord.Game(name="Helping people with Homebrew issues"),
            discord.Game(name=f"Watching **{server_count}** servers"),
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
bot.load_extension('Cogs.Auto_Features')

bot.run("TOKEN_HERE")
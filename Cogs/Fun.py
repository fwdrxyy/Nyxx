import discord
from discord.ext import commands
from discord import ui
import random
import sqlite3
import aiohttp

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'barn_counts.db'
        self.init_db()
         
    # Hug command
    @discord.slash_command(name="hug", description="Give someone a virtual hug!")
    async def hug(self, ctx, user: discord.Member):
        hug_messages = [
            f"{ctx.author.mention} gives {user.mention} a warm hug! ❤️",
            f"{ctx.author.mention} hugs {user.mention}! That's sweet! 🤗",
            f"{user.mention} receives a comforting hug from {ctx.author.mention}! 💕",
            f"{ctx.author.mention} wraps their arms around {user.mention}... *HUG* 🫂",
            f"Aww, {ctx.author.mention} hugs {user.mention}! 🥰",
            f"{ctx.author.mention} gives {user.mention} the biggest hug ever! 🤗💛",
        ]
        
        gif_url = await self.get_random_gif("hug")
        
        embed = discord.Embed(
            description=random.choice(hug_messages),
            color=discord.Color.pink()
        )
        if gif_url:
            embed.set_image(url=gif_url)
        await ctx.respond(embed=embed)
    
    async def get_random_gif(self, query):
        """Fetch a random GIF from Giphy API"""
        try:
            async with aiohttp.ClientSession() as session:
                # Using Giphy's public beta API key
                url = f"https://api.giphy.com/v1/gifs/search?q={query}&api_key=dc6zaTOxFJmzC&limit=50"
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data['data']:
                            gif = random.choice(data['data'])
                            return gif['images']['original']['url']
        except Exception as e:
            print(f"Error fetching GIF: {e}")
        return None
    
    # Slap command
    @discord.slash_command(name="slap", description="Playfully slap someone!")
    async def slap(self, ctx, user: discord.Member):
        slap_messages = [
            f"{ctx.author.mention} slaps {user.mention}! SMACK! 👋",
            f"{ctx.author.mention} gives {user.mention} a gentle slap! 💥",
            f"*SLAP* {ctx.author.mention} slaps {user.mention}! Did they deserve it? 👀",
            f"{user.mention} got slapped by {ctx.author.mention}! Ouch! 😵",
            f"{ctx.author.mention} unleashes a mighty slap on {user.mention}! 💫",
            f"WACK! {ctx.author.mention} slaps {user.mention}! That's gotta hurt! 🤕",
        ]
        
        gif_url = await self.get_random_gif("slap")
        
        embed = discord.Embed(
            description=random.choice(slap_messages),
            color=discord.Color.red()
        )
        if gif_url:
            embed.set_image(url=gif_url)
        await ctx.respond(embed=embed)
    
    # Rock Paper Scissors command
    @discord.slash_command(name="rps", description="Play Rock, Paper, Scissors against the bot!")
    async def rps(self, ctx, choice = discord.Option(str, choices=["rock", "paper", "scissors"])):
        choices_list = ["rock", "paper", "scissors"]
        bot_choice = random.choice(choices_list)
        user_choice = choice.lower()
        
        # Determine winner
        if user_choice == bot_choice:
            result = "It's a tie! 🤝"
        elif (user_choice == "rock" and bot_choice == "scissors") or \
             (user_choice == "paper" and bot_choice == "rock") or \
             (user_choice == "scissors" and bot_choice == "paper"):
            result = "You win!"
        else:
            result = "I win!"
        
        embed = discord.Embed(
            title="Rock, Paper, Scissors",
            color=discord.Color.blue(),
            description=f"**You chose:** {user_choice}\n**I chose:** {bot_choice}\n\n{result}"
        )
        await ctx.respond(embed=embed)
    
    # Ship command
    @discord.slash_command(name="ship", description="Ship two users together!")
    async def ship(self, ctx, user1: discord.Member, user2: discord.Member):
        # Generate compatibility percentage based on user IDs for consistency
        compatibility = ((user1.id + user2.id) % 101)
        
        # Create ship name from first half of user1 and second half of user2
        ship_name = user1.name[:len(user1.name)//2 + 1] + user2.name[len(user2.name)//2:]
        
        # Determine heart color based on compatibility
        if compatibility >= 80:
            color = discord.Color.red()
            reaction = "🔥 Perfect match!"
        elif compatibility >= 60:
            color = discord.Color.orange()
            reaction = "💕 Great connection!"
        elif compatibility >= 40:
            color = discord.Color.yellow()
            reaction = "💛 Could work!"
        else:
            color = discord.Color.blue()
            reaction = "💙 Hmm, maybe not..."
        
        embed = discord.Embed(
            title=f"📊 Shipping Report",
            color=color,
            description=f"**{user1.mention} + {user2.mention}**\n\nShip Name: **{ship_name}**\nCompatibility: **{compatibility}%**\n\n{reaction}"
        )
        
        # Add visual bar
        filled = int(compatibility / 10)
        empty = 10 - filled
        bar = "❤️" * filled + "🤍" * empty
        embed.add_field(name="Compatibility Bar", value=bar, inline=False)
        
        await ctx.respond(embed=embed)
        
    
    @discord.slash_command(name="barn", description="Barn a user! (a joke frome the Aurorachat Discord Server)")
    async def barn(self, ctx, user: discord.Member):
        user_id = str(user.id)
        count = self.increment_barn_count(user_id)
        await ctx.respond(f"get barned loser lol\n{user.mention} has been barned {count} times.")
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS barn_counts (user_id TEXT PRIMARY KEY, count INTEGER)''')
        conn.commit()
        conn.close()

    def get_barn_count(self, user_id):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('SELECT count FROM barn_counts WHERE user_id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else 0

    def increment_barn_count(self, user_id):
        count = self.get_barn_count(user_id) + 1
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('INSERT OR REPLACE INTO barn_counts (user_id, count) VALUES (?, ?)', (user_id, count))
        conn.commit()
        conn.close()
        return count

def setup(bot):
    bot.add_cog(Fun(bot))

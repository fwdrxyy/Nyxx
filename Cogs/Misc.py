import discord
from discord.ext import commands
import sqlite3

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = 'barn_counts.db'
        self.init_db()
        
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
    bot.add_cog(Misc(bot))
import discord
from discord.ext import commands, tasks
import asyncio
import aiohttp

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

class AutoFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Auto-Role
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(role)
        channel = discord.utils.get(member.guild.text_channels, name='welcome')
        await channel.send(f"Welcome to the server, {member.mention}! 🎉 You've been assigned the **Member** role. Enjoy your stay! <3")
        
    # Bad Words Filter (AutoMod)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        bad_words = ["nigga", "nga", "nigger", "fuck", "slut"] #will test when im home. at the time of typing this 9:47am. And Will add more later.
        
        if any(word in message.content.lower() for word in bad_words):
            try:
                await message.delete()
                await message.channel.send(
                    f"{message.author.mention}, watch your language!",
                    delete_after=5
                )
            except discord.Forbidden:
                print("Bot lacks permission to delete messages. Please update the bot perms via role or Contact the maker/owner of the bot to fix via Discord Dev Portal.")

        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(AutoFeatures(bot))
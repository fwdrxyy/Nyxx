import discord
from discord.ext import commands, tasks
import requests
import asyncio
import aiohttp

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)

Github_Repos = {
    "LumaTeam/Luma3DS": 1325817053264871536,
    "PabloMK7/CTGP-7updates": 1325820619073388565,
}
    
class AutoFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Github Releases for Nintendo Homebrew (Github Repos are the the top)
    @bot.event 
    async def on_ready(self):
        while True:
            for repo, channel_id in Github_Repos.items():
                channel = self.bot.get_channel(channel_id)
                if channel:
                    latest_release = await self.fetch_latest_release(repo)
                    if latest_release:
                        release_info = f"New release for {repo}: {latest_release['name']} - {latest_release['html_url']}"
                        await channel.send(release_info)
            await asyncio.sleep(3600)  # Check every hour for new releases

    async def fetch_latest_release(self, repo):
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None    
    # Auto-Role
    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(role)
        channel = discord.utils.get(member.guild.text_channels, name='║・𝐖𝐞𝐥𝐜𝐨𝐦𝐞')
        await channel.send(f"Welcome to the server, {member.mention}! 🎉 You've been assigned the **Member** role.")
        
    # Bad Words Filter (AutoMod)
    @commands.Cog.listener()
    async def on_message(self, message):
        bad_words = ["nigger", "nigga", "fuck", "bitch", "hoe",]
        if any(word in message.content.lower() for word in bad_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, watch your language! No bad words!")
        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(AutoFeatures(bot))

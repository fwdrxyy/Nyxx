import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

modmail_channel_id = "Channel ID Here"

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    # Check if the message is a DM
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            modmail_channel = self.bot.get_channel(modmail_channel_id)
            if modmail_channel:
                embed = discord.Embed(
                    title="New Modmail",
                    description=message.content,
                    color=discord.Color.green()
                )
                embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                embed.timestamp = message.created_at
                await modmail_channel.send(embed=embed)
                await message.reply("Your message has been forwarded to the staff. **Please wait for a stafff member to respond to your problem/issue.**")
            else:
                await message.reply("Error: Modmail channel not found. Please make a channel to make the system to work!")
                
def setup(bot):
    bot.add_cog(ModMail(bot))
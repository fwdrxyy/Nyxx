import discord
from discord.ext import commands, tasks

class Auto_Features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

    # Create Voice Channel
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            if len(after.channel.members) == 1:
                new_channel = await after.channel.guild.create_voice_channel(name=f"{member.name}'s Channel")
                await member.move_to(new_channel)
        elif before.channel is not None and after.channel is None:
            if len(before.channel.members) == 0:
                await before.channel.delete()

def setup(bot):
    bot.add_cog(Auto_Features(bot))

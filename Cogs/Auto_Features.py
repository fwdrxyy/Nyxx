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
        channel = discord.utils.get(member.guild.text_channels, name='welcome')
        await channel.send(f"Welcome to the server, {member.mention}! 🎉 You've been assigned the 'Member' role.")
        
    # Bad Words Filter
    @commands.Cog.listener()
    async def on_message(self, message):
        bad_words = ["nigger", "nigga", "fuck", "bitch", "hoe",]
        if any(word in message.content.lower() for word in bad_words):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, watch your language!")
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
          
# Reaction Roles (Add the role)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 1301976971382751312:  
            guild = self.bot.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name="Nyxx Updates")  # Role to assign
            member = guild.get_member(payload.user_id)
            if role:
                await member.add_roles(role)
                await member.send("You have been given the 'Nyxx Updates' role.")
                
    # Reaction Roles (Remove the role)
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 1301976971382751312:
            guild = self.bot.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, name="Nyxx Updates")  # Role to remove
            member = guild.get_member(payload.user_id)
            print(f"Trying to remove role from {member.name} in {guild.name}")  # Debug print
            if role and member:
                try:
                    await member.remove_roles(role)
                    await member.send("Your 'Nyxx Updates' role has been removed.")
                except discord.errors.Forbidden as e:
                    print(f"Error removing role from {member.name}: {e}")

    @discord.slash_command(name="add_reaction", description="Add a reaction to a message by its ID and channel ID")
    async def add_reaction(self, ctx, message_id: str, channel_id: str, emoji: str):
        try:
            message_id_int = int(message_id)
            channel = self.bot.get_channel(int(channel_id))
            message = await channel.fetch_message(message_id_int)
            print(f"Fetched message: {message.content}")  # Log the message content
            await message.add_reaction(emoji)
            await ctx.send(f"Reaction {emoji} added to message ID {message_id}.")
        except ValueError:
            await ctx.send("Invalid message ID or channel ID format. Please enter valid integers.")
        except discord.errors.NotFound:
            await ctx.send("Message not found.")
        except Exception as e:
            await ctx.send(f"Failed to add reaction: {e}")
            print(f"Error: {e}")  # Log the error



def setup(bot):
    bot.add_cog(Auto_Features(bot))

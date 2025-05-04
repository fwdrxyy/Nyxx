import discord
from discord.ext import commands
from discord.commands import Option

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None
        self.role_id = None
        self.emoji = None

    # Reaction Roles (Add the role)
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == self.message_id and str(payload.emoji) == self.emoji:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(self.role_id)
            member = guild.get_member(payload.user_id)
            print(f"Adding role to member: {member}, Role: {role}")  # Debug statement
            if role and member:
                try:
                    await member.add_roles(role)
                    await member.send(f"You have been given the *{role.name}* role.")
                except discord.Forbidden:
                    print(f"Failed to add role due to missing permissions for {member}")
                    await member.send("I'm unable to give you the role due to missing permissions.")
                except Exception as e:
                    print(f"Error adding role: {e}")

    # Reaction Roles (Remove the role)
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == self.message_id and str(payload.emoji) == self.emoji:
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(self.role_id)
            member = guild.get_member(payload.user_id)
            print(f"Removing role from member: {member}, Role: {role}")  # Debug statement
            if role and member:
                try:
                    await member.remove_roles(role)
                    await member.send(f"Your *{role.name}* role has been removed.")
                except discord.Forbidden:
                    print(f"Failed to remove role due to missing permissions for {member}")
                    await member.send("I'm unable to remove your role due to missing permissions.")
                except Exception as e:
                    print(f"Error removing role: {e}")

    @discord.slash_command(name="setup_reaction_roles", description="Setup a reaction role")
    async def setup_reaction_roles(self, ctx, channel_id: str, role_name: str, emoji: str, message_content: str):
        if any(role.name in ["Admins", "Moderators", "Owner", "Staff", "Head Admin", "Head Moderator", "Trainee Moderators"] for role in ctx.author.roles):
            try:
                channel_id = int(channel_id)  # Convert channel_id to integer
                channel = self.bot.get_channel(channel_id)

                if channel is None:
                    await ctx.respond("Invalid channel ID. Please ensure the channel ID is correct.")
                    return

                guild = ctx.guild
                role = discord.utils.get(guild.roles, name=role_name)
                if role is None:
                    role = await guild.create_role(name=role_name)
                    await ctx.respond(f"Role **{role_name}** created.")
                else:
                    await ctx.respond(f"Role **{role_name}** already exists. Using existing role.")

                message = await channel.send(message_content)
                await message.add_reaction(emoji)
                await ctx.respond(f"Message sent in {channel.name} with reaction {emoji}.")

                self.message_id = message.id
                self.role_id = role.id
                self.emoji = emoji
            except ValueError:
                await ctx.respond("Invalid channel ID format. Please enter a valid integer.")
            except Exception as e:
                await ctx.respond(f"Failed to set up reaction roles: {str(e)}")

def setup(bot):
    bot.add_cog(ReactionRoles(bot))

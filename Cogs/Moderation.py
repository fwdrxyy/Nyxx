import discord
from discord.ext import commands
from discord import Embed
from datetime import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Events
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hello there **{member.mention}**! Welcome to the server! Please read #rules and check the github section for updates! Enjoy your stay! <3'
        )
        
    # Slash commands for moderation
    @discord.slash_command(name="kick", description="Kick a user from the server")
    async def kick(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        if ctx.author.guild_permissions.kick_members:
            await member.kick(reason=reason)
            embed = Embed(title="User Kicked", description=f"{member.mention} has been kicked.", color=discord.Color.yellow)
            embed.add_field(name="Reason", value=reason, inline=False)
            # Adding the date and time to the footer
            embed.set_footer(text=f"Kicked by {ctx.author.name} | {datetime.utcnow().strftime('%m-%d-%Y %H:%M UTC')}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.respond(embed=embed)
        else:
            embed = Embed(title="Permission Denied", description="You don't have permission to kick members.", color=discord.Color.orange())
            await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(name="ban", description="Ban a user from the server")
    async def ban(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        if ctx.author.guild_permissions.ban_members:
            await member.ban(reason=reason)
            embed = Embed(title="User Banned", description=f"{member.mention} has been banned.", color=discord.Color.red())
            embed.add_field(name="Reason", value=reason, inline=False)
            # Adding the date and time to the footer
            embed.set_footer(text=f"Banned by {ctx.author.name} | {datetime.utcnow().strftime('%m-%d-%Y %H:%M UTC')}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            await ctx.respond(embed=embed)
        else:
            embed = Embed(title="Permission Denied!", description="You don't have permission to ban members!", color=discord.Color.red())
            await ctx.respond(embed=embed, ephemeral=True)
        await member.send(f"You have been banned from the server by a moderator, admin, or the owner. Reason: **{reason}**")

    @discord.slash_command(name="mute", description="Mute a user from the server")
    async def mute(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await member.edit(mute=True, reason=reason)
        embed = Embed(title="User Muted", description=f"{member.mention} has been muted.", color=discord.Color.darker_grey())
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Muted by {ctx.author.name} | {datetime.utcnow().strftime('%m-%d-%Y %H:%M UTC')}")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.respond(embed=embed)
        await member.send(f"You have been muted in the server by a moderator, admin, or the owner. Reason: **{reason}**")
        
        
    @discord.slash_command(name="unmute", description="Unmute a user from the server")
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not role:
            return await ctx.respond("The Muted role does not exist.", ephemeral=True)
        await member.remove_roles(role)
        await member.send(f"You have been unmuted in the server. Don't do whatever you did to get muted!")
        await ctx.respond(f"{member.mention} has been unmuted.")
        
    @discord.slash_command(name="warn", description="Warn a user from the server")
    async def warn(self, ctx, member: discord.Member, reason: str = "No reason provided"):
        embed = Embed(title="User Warned", description=f"{member.mention} has been warned.", color=discord.Color.orange())
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Warned by {ctx.author.name} | {datetime.utcnow().strftime('%m-%d-%Y %H:%M UTC')}")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.respond(embed=embed)
        await member.send(f"You have been warned in the server. Reason: **{reason}**")
        
    @discord.slash_command(name="unban", description="Unban a user from the server")
    async def unban(self, ctx, user_id: str):
        try:
            user = await self.bot.fetch_user(int(user_id))
            guild = ctx.guild
            await guild.unban(user)
            
            embed = Embed(title="User Unbanned", description=f"{user.mention} has been unbanned.", color=discord.Color.green())
            embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
            await ctx.respond(embed=embed)
            await user.send(f"You have been unbanned from the server. Don't do whatever you did to get banned again!")
        except Exception as e:
            await ctx.respond(f"An error occurred while unbanning the user: {str(e)}")
        except ValueError:
            await ctx.respond("Invalid user ID. Please enter a valid integer.")
        except discord.NotFound:
            await ctx.respond("User not found. Please check the user ID and try again.")


    
def setup(bot):
    bot.add_cog(Moderation(bot))

import discord
from discord.ext import commands
from discord import Embed
from datetime import datetime
import sqlite3

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("warnings.db") # Create a SQLite database for warnings
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS warnings (
                    user_id INTEGER PRIMARY KEY,
                    warning_count INTEGER DEFAULT 0
            )
        """)
    # Events
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hello there **{member.mention}**! Welcome to the server! Please read #rules and check the github section for updates! Enjoy your stay! <3'
        )
    
    async def warn_user(self, ctx, member, reason, guild, moderator):
        """Warns a user and tracks warning count"""
        user_id = member.id

        # Fetch current warnings or insert new record
        self.cursor.execute("SELECT warning_count FROM warnings WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()

        if result:
            warning_count = result[0] + 1
            self.cursor.execute("UPDATE warnings SET warning_count = ? WHERE user_id = ?", (warning_count, user_id))
        else:
            warning_count = 1
            self.cursor.execute("INSERT INTO warnings (user_id, warning_count) VALUES (?, ?)", (user_id, warning_count))

        self.conn.commit()

        embed = discord.Embed(title="User Warned", description=f"{member.mention} has been warned ({warning_count}/5).", color=discord.Color.orange())
        embed.add_field(name="Reason", value=reason, inline=False)
        embed.set_footer(text=f"Warned by {ctx.author.name} | {datetime.utcnow().strftime('%m-%d-%Y %H:%M UTC')}")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.respond(embed=embed)

        if warning_count >= 3:
            await member.kick(reason="Exceeded warning limit")
            await ctx.send(f"{member.mention} has been **kicked** for reaching 3 warnings. If they get two more, they're banned. ")

        if warning_count >= 5:
            await member.ban(reason="Excessive violations")
            await ctx.send(f"{member.mention} has been **banned** for reaching 5 warnings.")
            
    
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
        """Warns a user and triggers moderation action if needed"""
        await self.warn_user(ctx, member, reason)
        
    @discord.slash_command(name="check_warnings", description="View a user's warnings")
    async def check_warnings(self, ctx, member: discord.Member):
        self.cursor.execute("SELECT warning_count FROM warnings WHERE user_id = ?", (member.id,))
        result = self.cursor.fetchone()
        count = result[0] if result else 0

        await ctx.respond(f"{member.mention} has **{count} warnings**.")
        
    @discord.slash_command(name="reset_warnings", description="Reset a user's warnings")
    async def reset_warnings(self, ctx, member: discord.Member):
        self.cursor.execute("DELETE FROM warnings WHERE user_id = ?", (member.id,))
        self.conn.commit()
        await ctx.respond(f"{member.mention}'s warnings have been reset.")
        
    @discord.slash_command(name="reduce_warnings", description="Reduce a user's warnings by 1")
    async def reduce_warnings(self, ctx, member: discord.Member):
        self.cursor.execute("SELECT warning_count FROM warnings WHERE user_id = ?", (member.id,))
        result = self.cursor.fetchone()

        if result and result[0] > 0:
            self.cursor.execute("UPDATE warnings SET warning_count = warning_count - 1 WHERE user_id = ?", (member.id,))
            self.conn.commit()
            await ctx.respond(f"{member.mention}'s warnings have been **reduced by 1**.")
        else:
            await ctx.respond(f"{member.mention} has no warnings to reduce.")       
            
      
def setup(bot):
    bot.add_cog(Moderation(bot))
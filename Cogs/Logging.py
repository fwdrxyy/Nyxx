import discord
import random
from discord.ext import commands
from datetime import datetime

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def find_log_channel(self, guild):
        """Returns an existing log channel or defaults to a private staff/admin channel."""
        
        # Look for a log channel by common names
        log_channel_names = ["logs", "mod-log", "admin-log", "server-log"]
        
        for channel in guild.text_channels:
            if any(name in channel.name.lower() for name in log_channel_names):
                return channel  # Found a log channel, return it

        # If no log channel found, choose a random private admin/staff channel
        staff_channels = [
            ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages and ch.permissions_for(guild.owner).read_messages
        ]

        return random.choice(staff_channels) if staff_channels else None  # Pick random staff/admin channel if available

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """Handles bot joining a new server."""
        log_channel = self.find_log_channel(guild)

        if log_channel:
            embed = discord.Embed(
                title="Bot Joined",
                description=f"{self.bot.user.name} has joined {guild.name}.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Guild ID", value=guild.id, inline=True)
            embed.add_field(name="Member Count", value=guild.member_count, inline=True)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handles member joining."""
        log_channel = self.find_log_channel(member.guild)
        if log_channel:
            embed = discord.Embed(
                title="Member Joined",
                description=f"{member.name} has joined the server.",
                color=discord.Color.green()
            )
            embed.add_field(name="ID", value=member.id, inline=True)
            embed.add_field(name="Created at", value=member.created_at, inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Handles member leaving."""
        log_channel = self.find_log_channel(member.guild)

        if log_channel:
            embed = discord.Embed(
                title="Member Left",
                description=f"{member.name} has left the server.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID", value=member.id, inline=True)
            embed.add_field(name="Created at", value=member.created_at, inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Handles deleted messages."""
        log_channel = self.find_log_channel(message.guild)

        if log_channel:
            embed = discord.Embed(
                title="Message Deleted",
                description=f"A message from **{message.author.name}** was deleted.",
                color=discord.Color.dark_orange()
            )
            embed.add_field(name="Message Content", value=message.content or "[No Content]", inline=False)
            embed.add_field(name="Channel", value=message.channel.mention, inline=False)
            embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url)
            embed.set_footer(text=f"Deleted at {datetime.utcnow().strftime('%m-%d-%Y %H:%M UTC')}")

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_kick(self, member):
        """Handles member being kicked."""
        log_channel = self.find_log_channel(member.guild)

        if log_channel:
            embed = discord.Embed(
                title="Member Kicked",
                description=f"{member.mention} has been kicked.",
                color=discord.Color.orange()
            )
            embed.add_field(name="ID", value=member.id, inline=True)
            embed.add_field(name="Created at", value=member.created_at, inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        """Handles member being banned."""
        log_channel = self.find_log_channel(guild)

        if log_channel:
            embed = discord.Embed(
                title="Member Banned",
                description=f"{member.mention} has been banned.",
                color=discord.Color.red()
            )
            embed.add_field(name="ID", value=member.id, inline=True)
            embed.add_field(name="Created at", value=member.created_at, inline=True)
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

            await log_channel.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Logging(bot))
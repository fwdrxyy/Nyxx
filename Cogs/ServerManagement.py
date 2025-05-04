import discord
from discord.ext import commands

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Function to check if the user is the server owner or has a required role
    async def is_allowed(self, ctx):
        allowed_roles = ["Admins", "Moderators", "Owner", "Head Admin", "Head Moderator", "Trainee Moderator"]
        return ctx.author == ctx.guild.owner or any(role.name in allowed_roles for role in ctx.author.roles)

    # /announce command
    @commands.slash_command(name="announce", description="Send an announcement to a specific channel")
    async def announce(self, ctx, channel: discord.TextChannel, message: str):
        if await self.is_allowed(ctx):
            # Split the message into chunks of 2000 characters max
            for chunk in [message[i:i+2000] for i in range(0, len(message), 2000)]:
                await channel.send(chunk)
            
            await ctx.respond("Announcement sent!", ephemeral=True)
        else:
            await ctx.respond("You don't have permission to use this command!", ephemeral=True)

    # /slowmode command
    @discord.slash_command(name="slowmode", description="Set slow mode duration in a channel")
    async def slowmode(self, ctx, channel: discord.TextChannel, duration: int):
        if await self.is_allowed(ctx):
            await channel.edit(slowmode_delay=duration)
            await ctx.respond(f"Slow mode set to {duration} seconds in {channel.mention}", ephemeral=True)
        else:
            await ctx.respond("You don't have permission to use this command! Only the server owner and staff members are allowed to use this command!", ephemeral=True)

    # /lock command
    @discord.slash_command(name="lock", description="Lock a channel to prevent new messages")
    async def lock(self, ctx, channel: discord.TextChannel):
        if await self.is_allowed(ctx):
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.respond(f"{channel.mention} has been locked!", ephemeral=True)
        else:
            await ctx.respond("You don't have permission to use this command! Only the server owner and staff members are allowed to use this command!", ephemeral=True)

    # /unlock command
    @discord.slash_command(name="unlock", description="Unlock a previously locked channel")
    async def unlock(self, ctx, channel: discord.TextChannel):
        if await self.is_allowed(ctx):
            await channel.set_permissions(ctx.guild.default_role, send_messages=True)
            await ctx.respond(f"{channel.mention} has been unlocked!", ephemeral=True)
        else:
            await ctx.respond("You don't have permission to use this command! Only the server owner and staff members are allowed to use this command!", ephemeral=True)

    # /purge command
    @discord.slash_command(name="purge", description="Delete a specified number of messages")
    async def purge(self, ctx, amount: int):
        if await self.is_allowed(ctx):
            await ctx.channel.purge(limit=amount)
            await ctx.respond(f"Deleted {amount} messages!", ephemeral=True)
        else:
            await ctx.respond("You don't have permission to use this command! Only the server owner and staff members are allowed to use this command!", ephemeral=True)
            
    # /remove_slowmode command
    @discord.slash_command(name="remove_slowmode", description="Remove slow mode from a channel")
    async def remove_slowmode(self, ctx, channel: discord.TextChannel):
        if await self.is_allowed(ctx):
            await channel.edit(slowmode_delay=0)
            await ctx.respond(f"Slow mode has been removed from {channel.mention}!", ephemeral=True)
        else:
            await ctx.respond("You don't have permission to use this command! Only the server owner and staff members are allowed to use this command!", ephemeral=True)

def setup(bot):
    bot.add_cog(ServerManagement(bot))
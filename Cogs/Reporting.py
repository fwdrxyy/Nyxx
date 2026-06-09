import discord
from discord.ext import commands
from discord import Embed
from datetime import datetime

class Reporting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.REPORT_RECIPIENT_ID = None  # Will be set to bot owner if None
        
        #self.STAFF_ROLE_IDS = [123456789, 987654321, 555666777] #ignored for right now, but can be used to specify additional staff roles that should receive reports 
    
    async def get_report_recipients(self, guild):
        """Get all users who should receive reports (bot owner + staff members)"""
        recipients = set()
        
        # Add bot owner
        if self.REPORT_RECIPIENT_ID:
            recipients.add(self.REPORT_RECIPIENT_ID)
        elif self.bot.owner_id:
            recipients.add(self.bot.owner_id)
        
        # Add staff members with configured roles
        if self.STAFF_ROLE_IDS and guild:
            for role_id in self.STAFF_ROLE_IDS:
                role = guild.get_role(role_id)
                if role:
                    for member in role.members:
                        if not member.bot:  # Don't send to bots
                            recipients.add(member.id)
        
        return recipients

    @discord.slash_command(name="report", description="Report a user for breaking server rules")
    async def report(self, ctx, member: discord.Member, reason: str):
        """
        Report a user for breaking rules
        
        Parameters:
        member: The user to report
        reason: Why are you reporting them
        """
        
        # Prevent self-reporting
        if member == ctx.author:
            await ctx.respond("❌ You cannot report yourself!", ephemeral=True)
            return
        
        # Prevent reporting bots
        if member.bot:
            await ctx.respond("❌ You cannot report bot accounts!", ephemeral=True)
            return
        
        # Get all recipients for the report
        recipient_ids = await self.get_report_recipients(ctx.guild)
        
        if not recipient_ids:
            await ctx.respond("❌ Report system is not configured properly. Please contact an administrator.", ephemeral=True)
            return
        
        try:
            # Create the report embed
            report_embed = Embed(
                title="📋 New User Report",
                description=f"A user has submitted a report.",
                color=discord.Color.red()
            )
            
            report_embed.add_field(name="Reported User", value=f"{member.mention} ({member.id})", inline=False)
            report_embed.add_field(name="Reporter", value=f"{ctx.author.mention} ({ctx.author.id})", inline=False)
            report_embed.add_field(name="Reason", value=reason, inline=False)
            report_embed.add_field(name="Server", value=f"{ctx.guild.name} ({ctx.guild.id})", inline=False)
            report_embed.add_field(name="Report Time", value=f"<t:{int(datetime.utcnow().timestamp())}:f>", inline=False)
            
            # Add user avatars
            report_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            report_embed.set_footer(text=f"Reported by {ctx.author.name}")
            
            # Send DM to all recipients
            sent_count = 0
            for recipient_id in recipient_ids:
                try:
                    recipient = await self.bot.fetch_user(recipient_id)
                    await recipient.send(embed=report_embed)
                    sent_count += 1
                except discord.Forbidden:
                    pass  # Skip users with DMs disabled
                except Exception:
                    pass  # Skip any other errors
            
            if sent_count == 0:
                await ctx.respond("❌ Unable to send report. No recipients have DMs enabled.", ephemeral=True)
            else:
                # Confirm to the reporter (ephemeral so only they see it)
                await ctx.respond("✅ Your report has been submitted. Thank you for helping keep the server safe!", ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ An error occurred while submitting your report: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(Reporting(bot))

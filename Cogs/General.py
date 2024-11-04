import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Simple ping command
    @discord.slash_command(name="ping", description="Sends the bot's latency.")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! Latency is {self.bot.latency * 1000:.2f}ms")

    # Help command
    @discord.slash_command(name="commands", description="List of available commands.")
    async def help(self, ctx):
        help_message = """
    # List of Commands:
    /ping - Check bot latency
    
    /userinfo - Get information about a user
    
    /serverinfo - Get server information
    
    /rules - Displays the server rules. ONLY use this command in the #rules channel.
    """
        await ctx.respond(help_message)

    # User info command
    @discord.slash_command(name="userinfo", description="Gives information about a user.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        # Format the dates for readability
        joined_at = member.joined_at.strftime('%m-%d-%Y %H:%M:%S UTC') if member.joined_at else "Unknown"
        created_at = member.created_at.strftime('%m-%d-%Y %H:%M:%S UTC')
        
        embed = discord.Embed(
            title=f"{member.name}'s Info",
            description=f"Here is some information about {member.mention}.",
            color=discord.Color.blue()
        )
        
        # Add user's profile picture
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Add fields for user information
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick if member.nick else "No nickname", inline=True)
        embed.add_field(name="Joined Server", value=joined_at, inline=True)
        embed.add_field(name="Account Created", value=created_at, inline=True)
        embed.add_field(name="Highest Role", value=member.top_role.mention, inline=True)
        
        # Send the embed
        await ctx.respond(embed=embed)

    # Server info command
    @discord.slash_command(name="serverinfo", description="Gives information about the server.")
    async def serverinfo(self, ctx):
        guild = ctx.guild
        
        # Format the date for readability
        created_at = guild.created_at.strftime('%m-%d-%Y %H:%M:%S UTC')
        
        embed = discord.Embed(
            title=f"{guild.name}'s Info",
            description=f"Here is some information about the server **{guild.name}**.",
            color=discord.Color.green()
        )
        
        # Add server icon to the embed
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "No server icon")

        # Add fields for server information
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=created_at, inline=True)
        
        # Send the embed
        await ctx.respond(embed=embed)
        
    # Add more commands and features as needed
    @discord.slash_command(name="rules", description="Displays the server rules. ONLY use this command in the #rules channel.")
    async def rules(self, ctx):
        # Check if the command is used in the #rules channel
            rules = [
                "@everyone",
                "# Rules!!",
                "",
                "1. Be respectful to others. This is a friendly community and common sense applies.",
                "",
                "2. No spamming or flooding. Please do not post the same message multiple times. You can in the spam channel if there is a channel.",
                "",
                "3. No NSFW content. Any NSFW content found in ANY channel will be removed and the user will be warned. Too many warnings will result in a ban, kick or mute.",
                "",
                "4. No hate speech or discrimination. We do not tolerate any form of hate speech or discrimination.",
                "",
                "5. No Phishing Links To Malware, Screamers, IPs, Etc. This is a safe space for everyone. If you are caught doing this, you will be banned.",
                "",
                "6. No pinging randomly without a reason. If you need to ping someone, please do so in a respectful manner.",
                "",
                "7. Follow Discord's Terms of Service and Community Guidelines. https://discord.com/tos",
                "",
                "**More rules will be added soon in the future. Enjoy your stay here <3**",
            ]
            await ctx.respond("\n".join(rules))

def setup(bot):
    bot.add_cog(General(bot))

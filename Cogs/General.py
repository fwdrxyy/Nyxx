import discord
from discord.ext import commands
from discord import ui

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    class PaginatorView(ui.View):
        def __init__(self, pages):
            super().__init__(timeout=None)
            self.pages = pages
            self.current_page = 0
        
        def create_embed(self):
            embed = discord.Embed(title=f"Page {self.current_page + 1}/{len(self.pages)}", color=discord.Color.blue())
            embed.description = self.pages[self.current_page]
            return embed

        @ui.button(label="Next", style=discord.ButtonStyle.primary)
        async def next_button(self, button: ui.Button, interaction:  discord.Interaction):
            self.current_page = (self.current_page + 1) % len(self.pages)
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
        
        @ui.button(label="Previous", style=discord.ButtonStyle.primary) 
        async def prev_button(self, button: ui.Button, interaction: discord.Interaction): 
            self.current_page = (self.current_page - 1) % len(self.pages) 
            await interaction.response.edit_message(embed=self.create_embed(), view=self)
            
    @discord.slash_command(name="help", description="List all commands for Nyxx") 
    async def help(self, ctx): 
        pages = [] 
        for cog_name, cog in self.bot.cogs.items(): 
            cog_commands = cog.get_commands() 
            commands_list = "\n".join([f"/{cmd.name} - {cmd.description}" for cmd in cog_commands]) 
            if commands_list: 
                pages.append(f"**{cog_name}**\n{commands_list}") 
                
        view = self.PaginatorView(pages) 
        await ctx.respond(embed=view.create_embed(), view=view)
    
    # Simple ping command
    @discord.slash_command(name="ping", description="Sends the bot's latency.")
    async def ping(self, ctx):
        await ctx.respond(f"Pong! Latency is {self.bot.latency * 1000:.2f}ms")

    # User info command
    @discord.slash_command(name="userinfo", description="Gives information about a user.")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        
        # Format the dates for readability
        joined_at = member.joined_at.strftime('%m-%d-%Y %H:%M UTC') if member.joined_at else "Unknown"
        created_at = member.created_at.strftime('%m-%d-%Y %H:%M UTC')
        
        embed = discord.Embed(
            title=f"{member.name}'s Info",
            description=f"Here is some information about {member.mention}.",
            color=discord.Color.blue()
        )
        
        # Add user's profile picture
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Add fields for user information
        embed.add_field(name="User ID", value=member.id, inline=True)
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
        created_at = guild.created_at.strftime('%m-%d-%Y %H:%M UTC')
        
        embed = discord.Embed(
            title=f"{guild.name}'s Info",
            description=f"Here is some information about the server **{guild.name}**.",
            color=discord.Color.green()
        )
        
        # Add server icon to the embed
        embed.set_thumbnail(url=guild.icon.url if guild.icon else "No server icon")

        # Add fields for server information
        embed.add_field(name="Server ID", value=guild.id, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=created_at, inline=True)
        
        # Send the embed
        await ctx.respond(embed=embed)
        
    # Add more commands and features as needed
    @discord.slash_command(name="rules", description="Displays the server rules. ONLY use this command in the #rules channel.") 
    async def rules(self, ctx): 
        rules = [
            "1. All text channels are English only. Mods must be able to read all messages clearly. If you're a non English speaker, use a translator",
            "",
            "2. No harassment of others. Racism, sexism, xenophobia, transphobia, homophobia, misogyny, etc. are not allowed.", 
            "",
            "3. Keep all discussion civil and in the correct channels. Mods may asks you to move your conversation to the correct channel.", 
            "",
            "4. No inappropriate language. Remain respectful of others at all times.",
            "", 
            "5. Keep personal drama out of chat. Keep personal drama out of chat. Only in dms please",
            "",
            "6. No impersonation. Do not impersonate other users, moderators, and/or famous personalities.",
            "",
            "7. No spamming. Do not flood chat rooms with messages. Only allowed channel for spamming is #botspam", 
            "",
            "8. No NSFW content. Do not post or have conversations around NSFW content.", 
            "",
            "9. No inappropriate or offensive usernames, status's or profile pictures. You may be asked to change these if they violate our rules.", 
            "",
            "10. No politics. Talking about serious issues involving government officials, political parties, religions, or geo-political disagreements is not allowed. Even if these topics are approached in a civil manner, this is not the correct space for these conversations. Unless a channel is made for it"
            "",
            "11. No self-promotion, soliciting, or advertising. This also includes user DMs. #self-promo"
            "",
            "12. No malicious links. Any link that track IP addresses, or lead to malicious websites that contain malware will be removed."
            "",
            "13. Don't evade filters, This applies to both words and links. If something is censored, it is censored for a reason!"
            "",
            "14. Follow the Discord ToS and Community Guidelines. Terms of Service: https://discordapp.com/terms \nCommunity Guidelines: https://discord.com/guidelines"
            "",
            "15. **Staff hold final say**. Listen to and respect the volunteers that keep this server running."
        ] 
        embed = discord.Embed(title="Rules for my server(s)", description="\n".join(rules), color=0x00ff00) 
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))

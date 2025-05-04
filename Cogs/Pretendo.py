import discord
from discord.ext import commands

class Pretendo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Pretendo invite command
    @discord.slash_command(name="pretendo", description="Invite for the Pretendo Network Discord Server")
    async def pretendo(self, ctx):
        await ctx.respond("https://discord.gg/pretendo")
        
    # Install 3DS command
    @discord.slash_command(name="install3ds", description="Guide on how to install Pretendo on a Nintendo 3DS")
    async def install3ds(self, ctx):
        await ctx.respond("https://pretendo.network/docs/install/3ds")
        
    # Install Wii U command
    @discord.slash_command(name="installwiiu", description="Guide on how to install Pretendo on a Nintendo Wii U")
    async def installwiiu(self, ctx):
        await ctx.respond("https://pretendo.network/docs/install/wiiu")
        
    # Blogs command
    @discord.slash_command(name="blogs", description="Get a view of the Pretendo Network Blogs")
    async def blogs(self, ctx):
        await ctx.respond("https://pretendo.network/blog")
        
    # Progress command
    @discord.slash_command(name="progress", description="Get a view of the Pretendo Network progress on the games")
    async def progress(self, ctx):
        await ctx.respond("https://wiki.pretendo.zip/game-support-status")
        
    # Website command
    @discord.slash_command(name="website", description="Link to the Pretendo Network Website")
    async def website(self, ctx):
        await ctx.respond("https://pretendo.network")
        
    @discord.slash_command(name="serverstatus", description="Get the status of the Pretendo Network")
    async def serverstatus(self, ctx):
        await ctx.respond("https://status.pretendo.zip/")
        
def setup(bot):
    bot.add_cog(Pretendo(bot))
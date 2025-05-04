import discord
from discord.ext import commands

class Homebrews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(name="f3ds", description="Latest 3DS Firmware")
    async def f3ds(self,ctx):
        await ctx.respond(f"Current 3DS Firmware is: **11.17.0-50**.")

    @discord.slash_command(name="fwiiu", description="Latest Wii U Firmware")
    async def fwiiu(self, ctx):
        await ctx.respond(f"Current Wii U Firmware is: **5.5.6** for USA and **5.5.5** for Europe.")
        
    @discord.slash_command(name="ninhb", desciption="Invite for the Nintendo Homebrew discord server")
    async def ninhb(self, ctx):
        await ctx.respond("Heres the invite. If your stuck on some steps on the official guide(s) or just need help with general issues, Please join the server. People will gladly help you with your problem! https://discord.gg/nintendohomebrew")
        
    @discord.slash_command(name="cfw3ds", description="Guide on how to install CFW on a Nintendo 3DS")
    async def cfw3ds(self, ctx):
        await ctx.respond("Heres the guide to Install Custom Firmware on your 3DS https://3ds.hacks.guide/")
        
    @discord.slash_command(name="cfwwiiu", description="Guide on how to install CFW on a Nintendo Wii U")
    async def cfwwiiu(self, ctx):
        await ctx.respond("Heres the guide to Install Custom Firmware on your Wii U https://wiiu.hacks.guide/")

def setup(bot):
    bot.add_cog(Homebrews(bot))
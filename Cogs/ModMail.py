import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True  # Include DM messages

modmail_channel_id = "CHANNEL ID HERE"  # modmail channel ID
log_channel_id = "LOG ID HERE" # for logging

class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_threads = {} 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            modmail_channel = self.bot.get_channel(modmail_channel_id)
            if modmail_channel:
                embed = discord.Embed(
                    title="📬 New Modmail Message",
                    description=message.content,
                    color=discord.Color.green()
                )
                embed.set_author(name=message.author, icon_url=message.author.avatar.url)
                embed.set_footer(text=f"User ID: {message.author.id}")
                embed.timestamp = message.created_at

                sent_message = await modmail_channel.send(embed=embed)
                self.active_threads[sent_message.id] = message.author.id

                await message.reply("✅ Your message has been forwarded to the staff. Please wait for a response. We'll get back to you as soon as possible.")
            else:
                await message.reply("⚠️ Error: Modmail channel not found! Please make sure to make a modmail channel!")

    @discord.slash_command(name="reply", description="Reply to a user's modmail message.")
    async def reply(
        self,
        ctx: discord.ApplicationContext,
        user: discord.User,
        response: str,
    ):
        if ctx.channel.id != modmail_channel_id:
            await ctx.respond("❌ You can only use this command in the modmail channel.", ephemeral=True)
            return
        
        try:
            await user.send(f"📩 **Staff Response:**\n{response}")
            await ctx.respond(f"✅ Replied to {user.name}.", ephemeral=True)

            # Optional: log
            log_channel = self.bot.get_channel(log_channel_id)
            if log_channel:
                log_embed = discord.Embed(
                    title="📝 Modmail Log - Staff Reply",
                    description=response,
                    color=discord.Color.orange()
                )
                log_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar.url)
                log_embed.set_footer(text=f"Replied to {user.id}")
                log_embed.timestamp = discord.utils.utcnow()
                await log_channel.send(embed=log_embed)

        except discord.Forbidden:
            await ctx.respond("❌ Cannot send a DM to this user.", ephemeral=True)
        except Exception as e:
            await ctx.respond(f"⚠️ An error occurred: {e}", ephemeral=True)
            
def setup(bot):
    bot.add_cog(ModMail(bot))
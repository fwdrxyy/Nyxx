import discord
from discord.ext import commands

class Homebrews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.homebrew_guides = [
            {
                "name": "3ds firmware",
                "description": "Latest Nintendo 3DS firmware version.",
                "response": "Current 3DS Firmware is **11.17.0-50**.",
                "aliases": ["f3ds", "3ds fw", "3ds firmware"],
            },
            {
                "name": "wiiu firmware",
                "description": "Latest Nintendo Wii U firmware versions.",
                "response": "Current Wii U Firmware is **5.5.6** for USA and **5.5.5** for Europe.",
                "aliases": ["fwiiu", "wiiu fw", "wii u firmware"],
            },
            {
                "name": "nintendo homebrew discord",
                "description": "Invite link for the Nintendo Homebrew Discord server.",
                "url": "https://discord.gg/nintendohomebrew",
                "aliases": ["ninhb", "homebrew discord", "nintendo homebrew"],
            },
            {
                "name": "3ds cfw",
                "description": "Guide on how to install custom firmware on a Nintendo 3DS.",
                "url": "https://3ds.hacks.guide/",
                "aliases": ["cfw3ds", "3ds custom firmware", "3ds hax"],
            },
            {
                "name": "wiiu cfw",
                "description": "Guide on how to install custom firmware on a Nintendo Wii U.",
                "url": "https://wiiu.hacks.guide/",
                "aliases": ["cfwwiiu", "wiiu custom firmware", "wii u cfw"],
            },
            {
                "name": "pretendo network",
                "description": "Links and resources for the Pretendo Network.",
                "url": "https://pretendo.network",
                "aliases": ["pretendo", "pretendo network", "pretendo invite"],
            },
        ]

        self.homebrew_news = [
            {
                "title": "Pretendo Network Progress",
                "description": "Pretendo has updated its progress page with the latest game support status. (unofficial, but a good resource for tracking game compatibility)",
                "url": "https://wiki.pretendo.zip/game-support-status",
            },
            {
                "title": "3DS CFW Guide",
                "description": "The official 3DS Custom Firmware guide is still the best starting place for new homebrew users.",
                "url": "https://3ds.hacks.guide/",
            },
            {
                "title": "Wii U CFW Guide",
                "description": "The Wii U Custom Firmware guide is available for anyone installing homebrew on a Wii U.",
                "url": "https://wiiu.hacks.guide/",
            },
        ]

    @discord.slash_command(name="guide", description="Search homebrew guides, FAQs, and useful links")
    async def guide(self, ctx, topic: str = None):
        if topic is None:
            embed = discord.Embed(
                title="Homebrew Guide Search",
                description="Use `/guide <topic>` to search for homebrew resources. Examples: `3ds cfw`, `wiiu firmware`, `pretendo`, `ninhb`.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Popular topics",
                value="• 3ds cfw\n• wiiu cfw\n• 3ds firmware\n• wiiu firmware\n• nintendo homebrew\n• pretendo",
                inline=False,
            )
            await ctx.respond(embed=embed)
            return

        query = topic.lower().strip()
        matches = []
        for entry in self.homebrew_guides:
            haystack = " ".join([entry["name"], entry["description"]] + entry.get("aliases", [])).lower()
            if all(word in haystack for word in query.split()):
                matches.append(entry)

        if not matches:
            await ctx.respond(
                f"Sorry, I couldn't find anything for **{topic}**. Try `/guide` to see common homebrew topics."
            )
            return

        if len(matches) == 1:
            entry = matches[0]
            embed = discord.Embed(
                title=entry["name"].title(),
                description=entry["description"],
                color=discord.Color.green(),
            )
            if entry.get("response"):
                embed.add_field(name="Result", value=entry["response"], inline=False)
            if entry.get("url"):
                embed.add_field(name="Link", value=entry["url"], inline=False)
            await ctx.respond(embed=embed)
            return

        embed = discord.Embed(
            title="Homebrew Guide Results",
            description=f"Found {len(matches)} results for **{topic}**.",
            color=discord.Color.green(),
        )
        for entry in matches[:5]:
            value = entry.get("url", entry.get("response", "No link available."))
            embed.add_field(name=entry["name"].title(), value=value, inline=False)
        await ctx.respond(embed=embed)

    @discord.slash_command(name="homebrewnews", description="Get the latest homebrew news and updates")
    async def homebrewnews(self, ctx):
        embed = discord.Embed(
            title="Homebrew News",
            description="Latest homebrew updates and resource links.",
            color=discord.Color.gold(),
        )
        for item in self.homebrew_news:
            embed.add_field(
                name=item["title"],
                value=f"{item['description']}\n{item['url']}",
                inline=False,
            )
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Homebrews(bot))
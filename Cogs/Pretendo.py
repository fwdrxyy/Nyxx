import discord
from discord.ext import commands

class Pretendo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pretendo_resources = [
            {
                "name": "Pretendo Discord Invite",
                "description": "Invite for the Pretendo Network Discord Server.",
                "url": "https://discord.gg/pretendo",
                "aliases": ["invite", "discord", "pretendo invite"],
            },
            {
                "name": "Install Pretendo on 3DS",
                "description": "Guide on how to install Pretendo on a Nintendo 3DS.",
                "url": "https://pretendo.network/docs/install/3ds",
                "aliases": ["3ds", "install 3ds", "pretendo 3ds"],
            },
            {
                "name": "Install Pretendo on Wii U",
                "description": "Guide on how to install Pretendo on a Nintendo Wii U.",
                "url": "https://pretendo.network/docs/install/wiiu",
                "aliases": ["wiiu", "install wiiu", "pretendo wiiu"],
            },
            {
                "name": "Pretendo Blogs",
                "description": "Get a view of the Pretendo Network Blogs.",
                "url": "https://pretendo.network/blog",
                "aliases": ["blogs", "blog", "news"],
            },
            {
                "name": "Pretendo Progress",
                "description": "Get a view of the Pretendo Network progress on the games.",
                "url": "https://wiki.pretendo.zip/game-support-status",
                "aliases": ["progress", "status", "game support"],
            },
            {
                "name": "Pretendo Website",
                "description": "Link to the Pretendo Network Website.",
                "url": "https://pretendo.network",
                "aliases": ["website", "site", "homepage"],
            },
            {
                "name": "Pretendo Server Status",
                "description": "Get the game status of the Pretendo Network. an unofficial resource, but a good way to track game compatibility.",
                "url": "https://status.pretendo.zip/",
                "aliases": ["serverstatus", "status", "uptime"],
            },
        ]
        
    @discord.slash_command(name="pretendoguide", description="Search Pretendo Network links and resources")
    async def pretendoguide(self, ctx, topic: str = None):
        if topic is None:
            embed = discord.Embed(
                title="Pretendo Guide",
                description="Use `/pretendoguide <topic>` to find Pretendo resources.",
                color=discord.Color.blue(),
            )
            embed.add_field(
                name="Popular topics",
                value="• invite\n• install 3ds\n• install wiiu\n• blogs\n• progress\n• website\n• server status",
                inline=False,
            )
            await ctx.respond(embed=embed)
            return

        query = topic.lower().strip()
        matches = []
        for entry in self.pretendo_resources:
            haystack = " ".join([entry["name"], entry["description"]] + entry.get("aliases", [])).lower()
            if all(word in haystack for word in query.split()):
                matches.append(entry)

        if not matches:
            await ctx.respond(
                f"Sorry, I couldn't find anything for **{topic}**. Try `/pretendoguide` to see common Pretendo topics."
            )
            return

        if len(matches) == 1:
            entry = matches[0]
            embed = discord.Embed(
                title=entry["name"],
                description=entry["description"],
                color=discord.Color.green(),
            )
            embed.add_field(name="Link", value=entry["url"], inline=False)
            await ctx.respond(embed=embed)
            return

        embed = discord.Embed(
            title="Pretendo Guide Results",
            description=f"Found {len(matches)} results for **{topic}**.",
            color=discord.Color.green(),
        )
        for entry in matches[:5]:
            embed.add_field(name=entry["name"], value=entry["url"], inline=False)
        await ctx.respond(embed=embed)
        
    
def setup(bot):
    bot.add_cog(Pretendo(bot))
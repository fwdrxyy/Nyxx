from discord.ext import commands

from .AntiAbuse import AntiAbuse
from .Logging import Logging
from .Moderation import Moderation
from .Reporting import Reporting


class Administration(AntiAbuse, Moderation, Logging, Reporting):
    """Moderation commands, reports, and moderation logging."""

    def __init__(self, bot):
        AntiAbuse.__init__(self, bot)
        Moderation.__init__(self, bot)
        Logging.__init__(self, bot)
        Reporting.__init__(self, bot)


def setup(bot):
    bot.add_cog(Administration(bot))
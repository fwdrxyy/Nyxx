import asyncio
import sqlite3
from collections import defaultdict, deque
from datetime import timedelta

import discord
from discord.ext import commands


class AntiAbuse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect("anti_abuse.db")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS anti_abuse_settings (
                guild_id INTEGER PRIMARY KEY,
                spam_enabled INTEGER NOT NULL DEFAULT 1,
                raid_enabled INTEGER NOT NULL DEFAULT 1,
                spam_limit INTEGER NOT NULL DEFAULT 6,
                spam_window INTEGER NOT NULL DEFAULT 8,
                spam_timeout INTEGER NOT NULL DEFAULT 60,
                raid_limit INTEGER NOT NULL DEFAULT 8,
                raid_window INTEGER NOT NULL DEFAULT 10,
                raid_duration INTEGER NOT NULL DEFAULT 600,
                quarantine_role_id INTEGER
            )
        """)
        self.conn.commit()
        self._message_times = defaultdict(deque)
        self._next_message_state_cleanup = 0.0
        self._join_times = defaultdict(deque)
        self._raid_until = {}
        self._raid_locks = defaultdict(asyncio.Lock)

    def _get_settings(self, guild_id):
        row = self.conn.execute(
            """SELECT spam_enabled, raid_enabled, spam_limit, spam_window, spam_timeout,
                      raid_limit, raid_window, raid_duration, quarantine_role_id
               FROM anti_abuse_settings WHERE guild_id = ?""",
            (guild_id,),
        ).fetchone()
        if row is None:
            return {
                "spam_enabled": True,
                "raid_enabled": True,
                "spam_limit": 6,
                "spam_window": 8,
                "spam_timeout": 60,
                "raid_limit": 8,
                "raid_window": 10,
                "raid_duration": 600,
                "quarantine_role_id": None,
            }
        return dict(zip((
            "spam_enabled", "raid_enabled", "spam_limit", "spam_window", "spam_timeout",
            "raid_limit", "raid_window", "raid_duration", "quarantine_role_id",
        ), row))

    def _save_settings(self, guild_id, settings):
        self.conn.execute("""
            INSERT INTO anti_abuse_settings (
                guild_id, spam_enabled, raid_enabled, spam_limit, spam_window, spam_timeout,
                raid_limit, raid_window, raid_duration, quarantine_role_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(guild_id) DO UPDATE SET
                spam_enabled = excluded.spam_enabled,
                raid_enabled = excluded.raid_enabled,
                spam_limit = excluded.spam_limit,
                spam_window = excluded.spam_window,
                spam_timeout = excluded.spam_timeout,
                raid_limit = excluded.raid_limit,
                raid_window = excluded.raid_window,
                raid_duration = excluded.raid_duration,
                quarantine_role_id = excluded.quarantine_role_id
        """, (
            guild_id,
            int(settings["spam_enabled"]),
            int(settings["raid_enabled"]),
            settings["spam_limit"],
            settings["spam_window"],
            settings["spam_timeout"],
            settings["raid_limit"],
            settings["raid_window"],
            settings["raid_duration"],
            settings["quarantine_role_id"],
        ))
        self.conn.commit()

    async def _send_alert(self, guild, content):
        log_channel = self.find_log_channel(guild)
        if log_channel is None:
            return
        try:
            await log_channel.send(content)
        except discord.HTTPException:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is None or message.author.bot or message.webhook_id is not None:
            return

        member = message.author
        if member.guild_permissions.administrator or member.guild_permissions.manage_messages:
            return

        settings = self._get_settings(message.guild.id)
        if not settings["spam_enabled"]:
            return

        now = asyncio.get_running_loop().time()
        if now >= self._next_message_state_cleanup:
            stale_keys = [
                key for key, timestamps in self._message_times.items()
                if not timestamps or now - timestamps[-1] > 30
            ]
            for key in stale_keys:
                self._message_times.pop(key, None)
            self._next_message_state_cleanup = now + 30

        key = (message.guild.id, member.id)
        timestamps = self._message_times[key]
        cutoff = now - settings["spam_window"]
        while timestamps and timestamps[0] < cutoff:
            timestamps.popleft()
        timestamps.append(now)

        if len(timestamps) < settings["spam_limit"]:
            return

        timestamps.clear()
        try:
            await message.delete()
        except discord.HTTPException:
            pass

        try:
            await member.timeout_for(
                timedelta(seconds=settings["spam_timeout"]),
                reason="Anti-spam: message rate exceeded",
            )
        except discord.HTTPException:
            await self._send_alert(
                message.guild,
                f"Anti-spam detected rapid messages from {member.mention}, but I could not apply a timeout.",
            )
            return

        await self._send_alert(
            message.guild,
            f"Anti-spam timed out {member.mention} for {settings['spam_timeout']} seconds after rapid messages.",
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        settings = self._get_settings(member.guild.id)
        if not settings["raid_enabled"]:
            return

        now = asyncio.get_running_loop().time()
        guild_id = member.guild.id
        async with self._raid_locks[guild_id]:
            joins = self._join_times[guild_id]
            cutoff = now - settings["raid_window"]
            while joins and joins[0][0] < cutoff:
                joins.popleft()
            joins.append((now, member))
            join_count = len(joins)

            raid_active = now < self._raid_until.get(guild_id, 0)
            raid_started = not raid_active and join_count >= settings["raid_limit"]
            if raid_started:
                self._raid_until[guild_id] = now + settings["raid_duration"]
                members_to_quarantine = [joined_member for _, joined_member in joins]
            elif raid_active:
                members_to_quarantine = [member]
            else:
                members_to_quarantine = []

        role = member.guild.get_role(settings["quarantine_role_id"] or 0)
        if role is not None:
            for joined_member in members_to_quarantine:
                try:
                    await joined_member.add_roles(role, reason="Anti-raid quarantine")
                except discord.HTTPException:
                    if raid_started or joined_member.id == member.id:
                        await self._send_alert(
                            member.guild,
                            f"Raid protection could not quarantine {joined_member.mention}; check my Manage Roles permission and role position.",
                        )

        if raid_started:
            quarantine_note = f" New members are being assigned {role.mention}." if role else " Configure a quarantine role to restrict new arrivals."
            await self._send_alert(
                member.guild,
                f"Possible raid detected: {join_count} members joined within {settings['raid_window']} seconds. "
                f"Raid protection is active for {settings['raid_duration']} seconds.{quarantine_note}",
            )

    @discord.slash_command(name="anti_spam", description="Configure automatic spam protection")
    async def configure_anti_spam(
        self,
        ctx,
        enabled: bool,
        message_limit: int = 6,
        window_seconds: int = 8,
        timeout_seconds: int = 60,
    ):
        if ctx.guild is None or not ctx.author.guild_permissions.manage_guild:
            await ctx.respond("Manage Server permission is required.", ephemeral=True)
            return
        if not 3 <= message_limit <= 20 or not 2 <= window_seconds <= 30 or not 10 <= timeout_seconds <= 3600:
            await ctx.respond(
                "Use 3-20 messages, a 2-30 second window, and a 10-3600 second timeout.",
                ephemeral=True,
            )
            return

        settings = self._get_settings(ctx.guild.id)
        settings.update({
            "spam_enabled": enabled,
            "spam_limit": message_limit,
            "spam_window": window_seconds,
            "spam_timeout": timeout_seconds,
        })
        self._save_settings(ctx.guild.id, settings)
        state = "enabled" if enabled else "disabled"
        await ctx.respond(
            f"Anti-spam {state}: {message_limit} messages in {window_seconds} seconds triggers a {timeout_seconds}-second timeout.",
            ephemeral=True,
        )

    @discord.slash_command(name="anti_raid", description="Configure join-burst raid protection")
    async def configure_anti_raid(
        self,
        ctx,
        enabled: bool,
        join_limit: int = 8,
        window_seconds: int = 10,
        active_seconds: int = 600,
        quarantine_role: discord.Role = None,
    ):
        if ctx.guild is None or not ctx.author.guild_permissions.manage_guild:
            await ctx.respond("Manage Server permission is required.", ephemeral=True)
            return
        if not 3 <= join_limit <= 50 or not 2 <= window_seconds <= 60 or not 60 <= active_seconds <= 3600:
            await ctx.respond(
                "Use 3-50 joins, a 2-60 second window, and a 60-3600 second active period.",
                ephemeral=True,
            )
            return

        settings = self._get_settings(ctx.guild.id)
        settings.update({
            "raid_enabled": enabled,
            "raid_limit": join_limit,
            "raid_window": window_seconds,
            "raid_duration": active_seconds,
        })
        if quarantine_role is not None:
            settings["quarantine_role_id"] = quarantine_role.id
        self._save_settings(ctx.guild.id, settings)
        state = "enabled" if enabled else "disabled"
        role_note = f" Quarantine role: {quarantine_role.mention}." if quarantine_role else ""
        await ctx.respond(
            f"Anti-raid {state}: {join_limit} joins in {window_seconds} seconds activates protection for {active_seconds} seconds.{role_note}",
            ephemeral=True,
        )

    def cog_unload(self):
        self.conn.close()
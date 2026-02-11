import discord
from discord.ext import commands
from discord import Embed, Color

class RoleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_roles = ["Admins", "Moderators", "Owner", "Head Admin", "Head Moderator", "Trainee Moderator", "Staff"]

    async def is_allowed(self, ctx):
        """Check if user has permission to manage roles"""
        return ctx.author == ctx.guild.owner or any(role.name in self.allowed_roles for role in ctx.author.roles)

    @discord.slash_command(name="createrole", description="Create a new role")
    async def create_role(
        self,
        ctx,
        name: str,
        color: str = "random",
        hoist: bool = False,
    ):
        """Create a new role in the server"""
        if not await self.is_allowed(ctx):
            await ctx.respond("❌ You don't have permission to use this command!", ephemeral=True)
            return

        try:
            # Parse color
            if color.lower() == "random":
                role_color = discord.Color.random()
            else:
                # Remove # if present and convert hex to int
                color = color.lstrip('#')
                role_color = discord.Color(int(color, 16))

            role = await ctx.guild.create_role(
                name=name,
                color=role_color,
                hoist=hoist,
                mentionable=True
            )

            embed = Embed(
                title="✅ Role Created",
                description=f"Successfully created role {role.mention}",
                color=Color.green()
            )
            embed.add_field(name="Role Name", value=role.name, inline=True)
            embed.add_field(name="Role ID", value=role.id, inline=True)
            embed.add_field(name="Color", value=f"#{role.color.value:06x}", inline=True)
            embed.add_field(name="Hoist", value=str(hoist), inline=True)
            embed.set_footer(text=f"Created by {ctx.author.name}")

            await ctx.respond(embed=embed)

        except Exception as e:
            await ctx.respond(f"❌ Error creating role: {str(e)}", ephemeral=True)

    @discord.slash_command(name="deleterole", description="Delete a role")
    async def delete_role(self, ctx, role: discord.Role):
        """Delete a role from the server"""
        if not await self.is_allowed(ctx):
            await ctx.respond("❌ You don't have permission to use this command!", ephemeral=True)
            return

        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.respond("❌ You cannot delete a role equal to or higher than your own!", ephemeral=True)
            return

        if role == ctx.guild.default_role:
            await ctx.respond("❌ You cannot delete the @everyone role!", ephemeral=True)
            return

        try:
            role_name = role.name
            await role.delete()

            embed = Embed(
                title="✅ Role Deleted",
                description=f"Successfully deleted role **{role_name}**",
                color=Color.green()
            )
            embed.set_footer(text=f"Deleted by {ctx.author.name}")
            await ctx.respond(embed=embed)

        except Exception as e:
            await ctx.respond(f"❌ Error deleting role: {str(e)}", ephemeral=True)

    @discord.slash_command(name="assignrole", description="Assign a role to a user")
    async def assign_role(self, ctx, member: discord.Member, role: discord.Role):
        """Assign a role to a member"""
        if not await self.is_allowed(ctx):
            await ctx.respond("❌ You don't have permission to use this command!", ephemeral=True)
            return

        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.respond("❌ You cannot assign a role equal to or higher than your own!", ephemeral=True)
            return

        try:
            if role in member.roles:
                await ctx.respond(f"⚠️ {member.mention} already has the {role.mention} role!", ephemeral=True)
                return

            await member.add_roles(role)

            embed = Embed(
                title="✅ Role Assigned",
                description=f"Assigned {role.mention} to {member.mention}",
                color=Color.green()
            )
            embed.add_field(name="User", value=member.name, inline=True)
            embed.add_field(name="Role", value=role.name, inline=True)
            embed.set_footer(text=f"Assigned by {ctx.author.name}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

            await ctx.respond(embed=embed)

        except Exception as e:
            await ctx.respond(f"❌ Error assigning role: {str(e)}", ephemeral=True)

    @discord.slash_command(name="removerole", description="Remove a role from a user")
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
        """Remove a role from a member"""
        if not await self.is_allowed(ctx):
            await ctx.respond("❌ You don't have permission to use this command!", ephemeral=True)
            return

        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.respond("❌ You cannot remove a role equal to or higher than your own!", ephemeral=True)
            return

        try:
            if role not in member.roles:
                await ctx.respond(f"⚠️ {member.mention} doesn't have the {role.mention} role!", ephemeral=True)
                return

            await member.remove_roles(role)

            embed = Embed(
                title="✅ Role Removed",
                description=f"Removed {role.mention} from {member.mention}",
                color=Color.green()
            )
            embed.add_field(name="User", value=member.name, inline=True)
            embed.add_field(name="Role", value=role.name, inline=True)
            embed.set_footer(text=f"Removed by {ctx.author.name}")
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

            await ctx.respond(embed=embed)

        except Exception as e:
            await ctx.respond(f"❌ Error removing role: {str(e)}", ephemeral=True)

    @discord.slash_command(name="listroles", description="List all roles in the server")
    async def list_roles(self, ctx):
        """List all roles in the server"""
        try:
            roles = ctx.guild.roles[1:]  # Skip @everyone
            roles.reverse()  # Highest role first

            if not roles:
                await ctx.respond("No roles found in this server!", ephemeral=True)
                return

            # Create a list of roles with member counts
            role_list = []
            for role in roles[:20]:  # Limit to 20 roles to avoid exceeding embed limits
                member_count = len(role.members)
                role_list.append(f"{role.mention} - {member_count} members")

            embed = Embed(
                title="📋 Server Roles",
                description="\n".join(role_list),
                color=Color.blue()
            )
            embed.set_footer(text=f"Total roles: {len(roles)}")

            await ctx.respond(embed=embed)

        except Exception as e:
            await ctx.respond(f"❌ Error listing roles: {str(e)}", ephemeral=True)

    @discord.slash_command(name="roleinfo", description="Get information about a role")
    async def role_info(self, ctx, role: discord.Role):
        """Get detailed information about a role"""
        try:
            embed = Embed(
                title=f"Role Info: {role.name}",
                color=role.color if role.color != discord.Color.default() else Color.blue()
            )
            embed.add_field(name="Role ID", value=role.id, inline=True)
            embed.add_field(name="Color", value=f"#{role.color.value:06x}", inline=True)
            embed.add_field(name="Position", value=role.position, inline=True)
            embed.add_field(name="Members", value=len(role.members), inline=True)
            embed.add_field(name="Hoist", value="Yes" if role.hoist else "No", inline=True)
            embed.add_field(name="Mentionable", value="Yes" if role.mentionable else "No", inline=True)
            embed.add_field(name="Managed", value="Yes (Bot role)" if role.managed else "No", inline=True)
            embed.add_field(name="Created At", value=discord.utils.format_dt(role.created_at), inline=False)

            await ctx.respond(embed=embed)

        except Exception as e:
            await ctx.respond(f"❌ Error fetching role info: {str(e)}", ephemeral=True)

def setup(bot):
    bot.add_cog(RoleManagement(bot))

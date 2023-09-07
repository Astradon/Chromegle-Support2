import discord
from discord.ext import commands

class Lockdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.locked_channels = set()  # Keep track of locked channels
        self.allowed_role_id = 922249784012709920  # Replace with your role's ID

    def is_allowed_role(self, user):
        return any(role.id == self.allowed_role_id for role in user.roles)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        channel = ctx.channel

        # Check if the user has the allowed role
        if not self.is_allowed_role(ctx.author):
            await ctx.send("You do not have the required role to use this command.")
            return

        # Check if the channel is in the locked channels set
        if channel.id in self.locked_channels:
            # Unlock the channel by resetting permissions
            await channel.set_permissions(ctx.guild.default_role, send_messages=None)
            await ctx.send("This channel is no longer in lockdown.")
            # Remove the channel from the locked set
            self.locked_channels.remove(channel.id)
            
            # Send an embedded message indicating that the channel is unlocked
            unlock_embed = discord.Embed(
                title="Channel Unlocked",
                description=f"The channel {channel.mention} has been unlocked.",
                color=discord.Color.green()
            )
            await ctx.send(embed=unlock_embed)
        else:
            # Lock down the channel by removing send message permissions for @everyone
            await channel.set_permissions(ctx.guild.default_role, send_messages=False)
            await ctx.send("This channel is now in lockdown. Only users with the 'manage_channels' permission can send messages.")
            # Add the channel to the locked set
            self.locked_channels.add(channel.id)
            
            # Send an embedded message indicating that the channel is locked down
            lockdown_embed = discord.Embed(
                title="Channel Locked Down",
                description=f"The channel {channel.mention} has been locked down.",
                color=discord.Color.red()
            )
            await ctx.send(embed=lockdown_embed)

    @lock.error
    async def lock_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            # Create an embedded error message for insufficient permissions
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="You do not have the 'manage_channels' permission to use this command.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Lockdown(bot))
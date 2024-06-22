"""
MIT License

Copyright (c) 2021-present Kuro-Rui

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import discord
import kuroutils
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands.converter import CogConverter
from collections import defaultdict

class CogCount(kuroutils.Cog):
    """Count [botname]'s cogs, commands, servers, and users."""

    __author__ = ["Kuro, modified by Rosie"]
    __version__ = "0.0.4"

    def __init__(self, bot: Red):
        self.bot = bot
        self.command_usage = defaultdict(int)  # Track command usage per user

    async def initialize(self):
        self.bot.add_listener(self.on_command_completion, "on_command_completion")

    async def on_command_completion(self, ctx: commands.Context):
        user_id = ctx.author.id
        self.command_usage[user_id] += 1

    @commands.group()
    async def count(self, ctx: commands.Context):
        """See various counts related to [botname]."""
        pass

    @commands.is_owner()
    @count.command()
    async def cogs(self, ctx: commands.Context):
        """See how many cogs [botname] has."""

        total = len(set(await self.bot._cog_mgr.available_modules()))
        loaded = len(set(self.bot.extensions.keys()))
        unloaded = total - loaded

        description = (
            f"`Loaded   :` **{loaded}** Cogs.\n"
            f"`Unloaded :` **{unloaded}** Cogs.\n"
            f"`Total    :` **{total}** Cogs."
        )
        embed = discord.Embed(
            title="Cogs Count", description=description, color=await ctx.embed_color()
        )
        await ctx.send(embed=embed)

    @count.command()
    async def commands(self, ctx: commands.Context, cog: CogConverter = None):
        """
        See how many commands [botname] has.

        You can also provide a cog name to see how many commands are in that cog.
        The commands count includes subcommands.
        """
        if cog:
            commands = len(set(cog.walk_commands()))
            description = f"I have `{commands}` commands in that cog."
        else:
            commands = len(set(self.bot.walk_commands()))
            description = f"I have `{commands}` commands."

        embed = discord.Embed(
            title="Commands Count", description=description, color=await ctx.embed_color()
        )
        await ctx.send(embed=embed)

    @count.command()
    async def servers(self, ctx: commands.Context):
        """See how many servers [botname] is in."""
        servers = len(self.bot.guilds)
        description = f"I am in `{servers}` servers."

        embed = discord.Embed(
            title="Servers Count", description=description, color=await ctx.embed_color()
        )
        await ctx.send(embed=embed)

    @count.command()
    async def users(self, ctx: commands.Context):
        """See how many unique users [botname] is serving."""
        unique_users = len(set(self.bot.get_all_members()))
        description = f"I am serving `{unique_users}` unique users."

        embed = discord.Embed(
            title="Users Count", description=description, color=await ctx.embed_color()
        )
        await ctx.send(embed=embed)

    @count.command()
    async def usercommands(self, ctx: commands.Context, user_id: int):
        """See how many commands a specific user has run."""
        count = self.command_usage.get(user_id, 0)
        description = f"User with ID `{user_id}` has run `{count}` commands."

        embed = discord.Embed(
            title="User Commands Count", description=description, color=await ctx.embed_color()
        )
        await ctx.send(embed=embed)

def setup(bot):
    cog = CogCount(bot)
    bot.add_cog(cog)
    bot.loop.create_task(cog.initialize())

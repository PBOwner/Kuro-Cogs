import random
from random import choice

from io import BytesIO
import aiohttp

import discord

import redbot
from redbot.core import commands

from .images import food_images, food_emojis

class CursedImages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["cursedfoods"])
    async def cursedfood(self, ctx):
        """Generates a random cursed food image."""
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get("{}".format(random.choice(food_images))) as resp:
                    t = "Here's Cursed Food Image... {}".format(random.choice(food_emojis))
                    d = "⚠️**TW⚠️ : CURSED FOOD IMAGES**"
                    e = discord.Embed(title=t, description=d, color=await ctx.embed_color())
                    fn = "cursed_food.png"
                    f = ctx.message.attachments
                    f.filename = f"SPOILER_{fn}"
                    spoiler = await f.to_file()
                    await ctx.send(embed=e, file=spoiler)
"""
MIT License

Copyright (c) 2020 MyerFire

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

from discord.ext import commands
import discord
import humanfriendly


class Hypixel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.max_concurrency(1, per=commands.BucketType.user)
    async def hypixel(self, ctx, input_=None):
        player = await ctx.bot.hypixel.player.get(ctx=ctx, input_=input_)
        await ctx.send(embed=discord.Embed(
            color=player.rank.color,
            title=f"[{player.rank.name}] {player.name}"
        ).add_field(
            name="Level",
            value=f"{player.level.level} ({player.level.percentage}% to {player.level.next})"
        ).add_field(
            name="Karma",
            value=f"{player.karma:,d}"
        ).add_field(
            name="Achievement Points",
            value=f"{player.achievement_points:,d}"
        ).add_field(
            name="First Login",
            value=f"{player.logins.first.strftime(ctx.bot.static.CREATION_TIME_FORMAT)}\n"
                  f"{humanfriendly.format_timespan(ctx.bot.static.time() - player.logins.first)}"
        ).add_field(
            name="Last Login",
            value=f"{player.logins.last.strftime(ctx.bot.static.CREATION_TIME_FORMAT)}\n"
                  f"{humanfriendly.format_timespan(ctx.bot.static.time() - player.logins.last)}"
        ))


def setup(bot):
    bot.add_cog(Hypixel(bot))
    print("Reloaded cogs.minecraft.hypixel.hypixel")

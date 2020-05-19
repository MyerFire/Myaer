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

import core.static
from discord.ext import commands
import discord
from core.discord.markdown import Markdown
import core.minecraft.hypixel.request
from core.minecraft.hypixel.player.skywars import Skywars
from core.minecraft.request import MojangAPI
from core.minecraft.verification.verification import Verification

class SkywarsStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.hypixel = core.minecraft.hypixel.request.HypixelAPI()
        self.markdown = Markdown()
        self.mojang = MojangAPI()
        self.skywars = Skywars()
        self.verification = Verification()

    @commands.group(name = "sw", invoke_without_command = True)
    @commands.max_concurrency(1, per = commands.BucketType.user)
    async def skywars(self, ctx, *args):
        try:
            player = args[0]
            player_formatted_name = (await self.mojang.get_profile(player))['name']
            player_uuid = (await self.mojang.get_profile(player))['uuid']
        except IndexError: # If no arguments
            try:
                db_data = await self.verification.find_uuid(ctx.author.id)
                player_formatted_name = (await self.mojang.get_profile((db_data[0]['minecraft_uuid'])))['name']
                player_uuid = db_data[0]['minecraft_uuid']
            except IndexError:
                unverified_embed = discord.Embed(
                    name = "Not verified",
                    description = "You have to verify with `/mc verify <minecraft-ign>` first."
                )
                await ctx.send(embed = unverified_embed)
                return
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player}\" is not a valid username or UUID."
            )
            await ctx.send(embed = nameerror_embed)
            return
        loading_embed = discord.Embed(
            name = "Loading",
            description = f"Loading {player_formatted_name}\'s Skywars stats..."
        )
        message = await ctx.send(embed = loading_embed)
        try:
            await self.hypixel.send_player_request_uuid(player_uuid) # Triggers request and sets global variable "player_json" in core.minecraft.hypixel.request
        except NameError:
            nameerror_embed = discord.Embed(
                name = "Invalid input",
                description = f"\"{player_formatted_name}\" does not seem to have Hypixel stats."
            )
            await ctx.send(embed = nameerror_embed)
            return
        player_stats_embed = discord.Embed(
            title = (await self.markdown.bold(f"{discord.utils.escape_markdown(player_formatted_name)}\'s Skywars Stats")),
            color = int((await self.skywars.get_prestige_data())['prestige_color'], 16) # 16 - Hex value.
        )
        player_stats_embed.set_thumbnail(
            url = core.static.hypixel_game_icons['Skywars']
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Level"))),
            value = f"{await self.skywars.get_star()} {core.static.bedwars_star} ({(await self.skywars.get_prestige_data())['prestige']} Prestige)",
            inline = False
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Coins"))),
            value = f"{await self.skywars.get_coins()}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Tokens"))),
            value = f"{await self.skywars.get_tokens()}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Souls"))),
            value = f"{await self.skywars.get_souls()}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Kills"))),
            value = f"{await self.skywars.get_kills()}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Deaths"))),
            value = f"{await self.skywars.get_deaths()}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} KDR"))),
            value = f"{(await self.skywars.get_ratio((await self.skywars.get_kills()), (await self.skywars.get_deaths())))}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Wins"))),
            value = f"{await self.skywars.get_wins()}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} Losses"))),
            value = f"{await self.skywars.get_losses()}"
        )
        player_stats_embed.add_field(
            name = await self.markdown.underline((await self.markdown.bold(f"{core.static.arrow_bullet_point} WLR"))),
            value = f"{(await self.skywars.get_ratio((await self.skywars.get_wins()), (await self.skywars.get_losses())))}"
        )
        await message.edit(embed = player_stats_embed)

def setup(bot):
    bot.add_cog(SkywarsStats(bot))
    print("Reloaded cogs.minecraft.hypixel.skywars")

import asyncio
import discord as d
from discord.ext import commands as cmds
import datetime as dt
from settings import BUMP_ROLE_ID, DISBOARD_BOT_ID, DISSOKU_BOT_ID


async def _send_bump_notification(message: d.Message, command_name: str, delay: int):
    now = dt.datetime.now()
    next_bump = now + dt.timedelta(hours=delay)

    embed = d.Embed(title=f"「/{command_name}」が実行されました！",
                    colour=d.Colour.blue())
    embed.add_field(name="実行された日時",
                    value=f"{now.hour}時{now.minute}分{now.second}秒")
    embed.add_field(name="次回実行可能になる日時",
                    value=f"{next_bump.hour}時{next_bump.minute}分{next_bump.second}秒")

    await message.channel.send(embed=embed)
    await asyncio.sleep(delay)

    role = message.guild.get_role(BUMP_ROLE_ID)
    mention = role.mention if role else ""

    embed = d.Embed(title="「/{command_name}」が実行可能になりました！",
                    colour=d.Colour.teal())

    await message.channel.send(mention, embed=embed)


class BumpNotice(cmds.Cog):
    def __init__(self, bot: cmds.Bot):
        self.bot = bot

    @cmds.Cog.listener(name="on_message")
    async def bump(self, message: d.Message):
        if message.author.id != DISBOARD_BOT_ID:
            return

        if not message.embeds:
            return

        embed = message.embeds[0]
        if not embed.description or "表示順をアップしたよ" not in embed.description:
            return

        await _send_bump_notification(message, "bump", 2)

    @cmds.Cog.listener(name="on_message_edit")
    async def dissoku_up(self, b: d.Message, a: d.Message):
        if not a or a.author.id != DISSOKU_BOT_ID or not a.embeds:
            return

        if not a.embeds[0].fields or "をアップしたよ" not in a.embeds[0].fields[0].name:
            return

        await _send_bump_notification(a, "dissoku_up", 2)


async def setup(bot: cmds.Bot):
    await bot.add_cog(BumpNotice(bot))

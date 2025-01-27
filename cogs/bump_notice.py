import asyncio

import discord as d
from discord.ext import commands as cmds
import datetime as dt


class BumpNotice(cmds.Cog):
    def __init__(self, bot: cmds.Bot):
        self.bot = bot

    @cmds.Cog.listener(name="on_message")
    async def bump(
            self,
            message: d.Message
    ):
        if message is None:
            return

        # メッセージ元のidがDISBOARDと一致するか比較...さすればよきかな
        if message.author.id != 302050872383242240:
            return

        if message.embeds is None:
            return

        # embedのdescriptionが「表示順をアップしたよ」で始まるか...さすればいい感じだろう
        if not message.embeds[0].description.startswith('表示順をアップしたよ'):
            return

        now = dt.datetime.now()
        next_bump = now + dt.timedelta(hours=1)

        embed = d.Embed(
            title='「/bump」が実行されました！',
            colour=d.Colour.blue()
        )
        embed.add_field(
            name='実行された日時',
            value=f'{now.hour}時{now.minute}分{now.second}秒'
        )
        embed.add_field(
            name='次回実行可能になる日時',
            value=f'{next_bump.hour}時{next_bump.minute}分{next_bump.second}秒'
        )

        await message.channel.send(embed=embed)

        # １時間後の通知用だっぴ
        await asyncio.sleep(3600)

        embed = d.Embed(
            title='「/bump」が実行可能になりました！',
            colour=d.Colour.teal()
        )

        return await message.channel.send(
            embed=embed
        )

    @cmds.Cog.listener(name="on_message_edit")
    async def dissoku_up(
            self,
            b: d.Message,
            a: d.Message
    ):
        if a is None:
            return

        if a.embeds is None:
            return

        if a.embeds[0].description.find('をアップしたよ!') < 0:
            return

        now = dt.datetime.now()
        next_bump = now + dt.timedelta(hours=1)

        embed = d.Embed(
            title='「/dissoku up」が実行されました！',
            colour=d.Colour.blue()
        )
        embed.add_field(
            name='実行された日時',
            value=f'{now.hour}時{now.minute}分{now.second}秒'
        )
        embed.add_field(
            name='次回実行可能になる日時',
            value=f'{next_bump.hour}時{next_bump.minute}分{next_bump.second}秒'
        )

        await a.channel.send(embed=embed)

        # １時間後の通知用だっぴ
        await asyncio.sleep(3600)

        embed = d.Embed(
            title='「/dissoku up」が実行可能になりました！',
            colour=d.Colour.teal()
        )

        return await a.channel.send(
            embed=embed
        )


async def setup(bot: cmds.Bot):
    await bot.add_cog(BumpNotice(bot))

import asyncio
import discord as d
from discord.ext import commands as cmds
import datetime as dt
import settings as s


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
        if message.embeds[0].description.find('表示順をアップしたよ') < 0:
            return

        now = dt.datetime.now()
        next_bump = now + dt.timedelta(hours=2)

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
        await asyncio.sleep(7)

        role = message.guild.get_role(s.bump_role_id)

        embed = d.Embed(
            title='「/bump」が実行可能になりました！',
            colour=d.Colour.teal()
        )

        if role is not None:
            return await message.channel.send(
                role.mention,
                embed=embed
            )
        else:
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

        if a.author.id != 761562078095867916:
            return

        if a.embeds is None:
            return

        if a.embeds[0].fields[0].name is None:
            return

        if a.embeds[0].fields[0].name.find('をアップしたよ') < 0:
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
        await asyncio.sleep(3)

        role = a.guild.get_role(s.bump_role_id)

        embed = d.Embed(
            title='「/dissoku up」が実行可能になりました！',
            colour=d.Colour.teal()
        )

        if role is not None:
            return await a.channel.send(
                role.mention,
                embed=embed
            )
        else:
            return await a.channel.send(
                embed=embed
            )


async def setup(bot: cmds.Bot):
    await bot.add_cog(BumpNotice(bot))

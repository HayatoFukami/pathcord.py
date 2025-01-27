import discord as d
from discord.ext import commands as cmds
import settings as s


class MyBot(cmds.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents=d.Intents.all()
        )

    async def setup_hook(self) -> None:
        if s.cogs is not None:
            for cog in s.cogs:
                await self.load_extension(cog)
                print(f'Loaded {cog}')
        # await self.tree.sync()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')


if __name__ == '__main__':
    bot = MyBot()
    bot.run(s.TOKEN)

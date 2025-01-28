import os
from dotenv import load_dotenv
import discord as d
from discord.ext import commands as cmds
from settings import COGS


class MyBot(cmds.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='/',
            intents=d.Intents.all()
        )

    async def setup_hook(self) -> None:
        if COGS is not None:
            for cog in COGS:
                await self.load_extension(cog)
                print(f"Loaded {cog}")
        # await self.tree.sync()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("PATHCORD_TOKEN")
    bot = MyBot()
    bot.run(token)

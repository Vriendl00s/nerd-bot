from db_connection import db_conn
import discord
import vacefron
import random
import math
from discord.ext import commands
from randomcommands import leveling

class Leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        await leveling.handle_message(message)


async def setup(bot):
    await bot.add_cog(Leveling(bot))
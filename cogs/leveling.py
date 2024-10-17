from db_connection import db_conn
import discord
import vacefron
import random
import math
from discord.ext import commands

class Leveling(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        query = f"""
        SELECT * FROM levels
        WHERE user_id = {message.author.id}
        AND server_id = {message.guild.id}
        """
        result = db_conn(query)

        if result == []:
            query = f"""
            INSERT INTO levels (user_id, server_id, xp, level)
            VALUES ({message.author.id}, {message.guild.id}, 0, 0)
            """
            db_conn(query, commit=True)

        else:
            xp = result[0][2]
            level = result[0][3]

            xp_gained = random.randint(1,15)
            xp += xp_gained
            new_lvl = math.floor(0.1 * math.sqrt(xp))

            if new_lvl > level:
                query = f"""
                UPDATE levels
                SET xp = {xp}, level = {new_lvl}
                WHERE user_id = {message.author.id}
                AND server_id = {message.guild.id}
                """
                db_conn(query, commit=True)

                await message.channel.send(f"Congrats {message.author.mention}! You have leveled up to level {new_lvl}!")
            else:
                query = f"""
                UPDATE levels
                SET xp = {xp}
                WHERE user_id = {message.author.id}
                AND server_id = {message.guild.id}
                """
                db_conn(query, commit=True)

async def setup(bot):
    await bot.add_cog(Leveling(bot))
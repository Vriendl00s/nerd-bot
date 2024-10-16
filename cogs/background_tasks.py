import discord
from discord.ext import commands, tasks
from db_connection import db_conn

class BackgroundTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check_users.start()

    def cog_unload(self) -> None:
        self.check_users.stop()
        
    # Check the status of all users in all guilds every 5 minutes
    @tasks.loop(seconds=300)
    async def check_users(self):
        query = "SELECT * FROM online_channel"
        result = db_conn(query)

        if result != []:
            for guild in result:
                channel_id = guild[0]
                guild_id = guild[1]

                server = self.bot.get_guild(guild_id)

                online = 0

                for member in server.members:
                    if member.status == discord.Status.online or member.status == discord.Status.dnd or member.status == discord.Status.idle:
                        online += 1

                
                # TO DO: Dynamic channel instead of hardcoded channel id
                channel = discord.utils.get(server.channels, id=channel_id)
                if channel:
                    await channel.edit(name=f"Online: {online}")
            

async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))  
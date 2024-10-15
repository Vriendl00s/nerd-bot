import discord
from discord.ext import commands, tasks

class BackgroundTasks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.check_users.start()

    def cog_unload(self) -> None:
        self.check_users.stop()
        
    # Check the status of all users in all guilds every 5 minutes
    @tasks.loop(seconds=300)
    async def check_users(self):
        for guild in self.bot.guilds:
            online = 0
            offline = 0
            dnd = 0
            idle = 0

            for member in guild.members:
                if member.status == discord.Status.online:
                    online += 1
                elif member.status == discord.Status.offline:
                    offline += 1
                elif member.status == discord.Status.dnd:
                    dnd += 1
                elif member.status == discord.Status.idle:
                    idle += 1
            
            # TO DO: Dynamic channel instead of hardcoded channel id
            channel = discord.utils.get(guild.channels, id=1295872523917070418)
            if channel:
                await channel.edit(name=f"Online: {online}")
            

async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))  
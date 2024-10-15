import discord
from discord.ext import commands
from standardutils.reply import reply
from standardutils.parsed_time import parsed_time
import datetime

async def remindme(ctx, message, time):
    """Remind the user of something after a certain amount of time."""
    time = parsed_time(time, ctx)

    if time is None:
        return reply(ctx, "Invalid time format. Ensure the format is <number><unit> (e.g., 1h, 2d).")
    try:
        await ctx.author.send(f"Reminder: {message}")
    except discord.Forbidden:
        await reply(ctx, message)
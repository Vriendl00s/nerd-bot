from datetime import timedelta

async def parsed_time(time, ctx):
    """variable 'time' will be in the format of <number><unit> (e.g., 1h, 2d)."""

    """Parse a time string into a datetime object."""
    units = {
        's': 1,
        'm': 60,
        'h': 3600,
        'D': 86400,
        'W': 604800,
        'M': 2592000,
        'Y': 31536000
    }
    
    unit = time[-1]
    if unit not in units:
        await ctx.author.reply("Invalid time unit. Use 'h', 'd', 'w', 'm', or 'y'.")
        return None
    
    try:
        value = int(time[0])
    except ValueError:
        await ctx.author.reply("Invalid time format. Ensure the format is <number><unit> (e.g., 1h, 2d).")
        return None
    
    length = timedelta(seconds=value * units[unit])

    return length



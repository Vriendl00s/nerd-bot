import discord
from standardutils.reply import reply
from standardutils.parsed_time import parsed_time
from standardutils.get_author import get_author
import datetime
from db_connection import db_conn

async def remindme_save(ctx, message, time):
    """Remind the user of something after a certain amount of time."""

    author = await get_author(ctx)
    # Determine at what time to remind
    length = await parsed_time(time, ctx)
    time = datetime.datetime.now() + length
    time = time.strftime('%Y-%m-%d %H:%M:%S')

    query = f"""INSERT INTO reminders (user_id, message, time)
                VALUES ({author.id}, '{message}', '{time}')"""
    db_conn(query, commit=True)
    
    await reply(ctx, f"Reminder set for {time}. Make sure to have DMs enabled to receive the reminder.")



async def remindme_send(bot):
    """Send reminders to users."""

    # Check if time has passed for any reminders
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    query = f"""SELECT * FROM reminders
                WHERE time < '{current_time}'"""
    
    results = db_conn(query)

    # send each reminder and delete from the db
    for reminder in results:
        user = await bot.fetch_user(reminder[0])
        message = reminder[1]
        time = reminder[2]

        try:
            await user.send(f"Reminder: {message}")
        except discord.HTTPException:
            pass

        query = f"""DELETE FROM reminders
                    WHERE user_id = {user.id}
                    AND message = '{message}'
                    AND time = '{time}'"""
        db_conn(query, commit=True)

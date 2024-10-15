import discord
from discord.ext import commands
import json
import sqlite3
from datetime import datetime, timedelta
from db_connection import db_conn 
from standardutils.reply import reply
from standardutils.parsed_time import parsed_time

async def check_admin(ctx, user=None):
    try:
        author = ctx.author
    except AttributeError:
        author = ctx.user
    
    try:
        if author.top_role <= user.top_role:
            await reply(ctx, "You cannot ban this user since they have a higher role than you.")
            return
    except:
        pass
    
    if author.guild_permissions.administrator is False:
        await reply(ctx, "You do not have permission to ban users.")
        return

    return author


async def ban(ctx, user, length=None, reason=None):
    
    author = await check_admin(ctx, user)

    if reason is None:
        reason = "No reason provided."
    
    message = reason
    message += f" | Banned by {author}"

    if length is not None:
        message += f" | Length: {length}"
        length = await parsed_time(length, ctx)
        length = datetime.now() + length

        query = f"""
        INSERT INTO moderation (UID, server_id, type, until, reason) 
        VALUES ({user.id}, {ctx.guild.id}, 'BAN', '{length}', '{reason}')
        """

        db_conn(query, commit=True)
    else:
        message += " | Permanent"
        length = None


    await ctx.guild.ban(user, reason=message)

    try: 
        await user.send(f"You have been banned from {ctx.guild.name} | {message}.")
    except discord.HTTPException:
        pass

    await reply(ctx, f"Banned {user.name} | {message}.")



async def unban(ctx, user):

    author = await check_admin(ctx, user)
    """Unban a user from the server."""
    await ctx.guild.unban(user)

    query = f"""
    SELECT * FROM moderation 
    WHERE UID = {user.id} 
    AND server_id = {ctx.guild.id} 
    AND type = 'BAN'
    """

    result = db_conn(query)
    if result is not None:

        query = f"""
        DELETE FROM moderation 
        WHERE UID = {user.id} 
        AND server_id = {ctx.guild.id} 
        AND type = 'BAN'
        """

        db_conn(query, commit=True)

    await reply(ctx, f"Unbanned {user.name}.")



async def kick(ctx, user, reason=None):

    author = await check_admin(ctx, user)
    """Kick a user from the server."""
    if reason is None:
        reason = "No reason provided."
    await ctx.guild.kick(user, reason=reason)
    await reply(ctx, f'Kicked {user.name} | {reason}.')



async def mute(ctx, user, length=None, reason=None):

    author = await check_admin(ctx, user)
    """Mute a user in the server."""
    if reason is None:
        reason = "No reason provided."

    message = reason

    if length is not None:
        message += f" | Length: {length}"
        length = await parsed_time(length, ctx)
        length = datetime.now() + length

        query = f"""
        INSERT INTO moderation (UID, server_id, type, until, reason) 
        VALUES ({user.id}, {ctx.guild.id}, 'MUTE', '{length}', '{reason}')
        """

        db_conn(query, commit=True)
    else:
        message += " | Permanent"
        length = None

    # Create the muted role if it does not exist
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role is None:
        muted_role = await ctx.guild.create_role(name="Muted")

    # Set permissions for the muted role in all channels if not already set
    for channel in ctx.guild.channels:
        await channel.set_permissions(muted_role, send_messages=False)

    await user.add_roles(muted_role)
    await reply(ctx, f"Muted {user.name} | {message}.")



async def unmute(ctx, user):

    author = await check_admin(ctx, user)
    """Unmute a user in the server."""

    query = f"""
    DELETE FROM moderation 
    WHERE UID = {user.id} 
    AND server_id = {ctx.guild.id} 
    AND type = 'MUTE'
    """

    db_conn(query, commit=True)

    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role is None:
        await reply(ctx, "Muted role not found. Please create a 'Muted' role.")
        return
    await user.remove_roles(muted_role)

    await reply(ctx, f"Unmuted {user.name}.")



async def warn(ctx, user, reason=None):

    author = await check_admin(ctx, user)
    """Warn a user in the server."""
    if reason is None:
        reason = "No reason provided."
    
    query = f'INSERT INTO moderation (UID, server_id, type, until, reason) VALUES ({user.id}, {ctx.guild.id}, "WARN", "None", "{reason}")'
    db_conn(query, commit=True)

    await reply(ctx, f"Warned {user.name} | {reason}.")



async def clear(ctx, amount=5):
    
    author = await check_admin(ctx)
    try:
        await ctx.response.defer()
    except:
        pass
    await ctx.channel.purge(limit=amount)
    await reply(ctx, f"Cleared {amount} messages.")


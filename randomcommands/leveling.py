from standardutils.get_author import get_author
from db_connection import db_conn
import vacefron
from discord import File
import io
import random
import math
import discord


async def check_level(ctx):
    # Get the author of the message.
    author = await get_author(ctx)

    # Query to get the user's XP and level from the database.
    query1 = f"""SELECT xp, level 
                FROM levels 
                WHERE user_id = {author.id} 
                AND server_id = {ctx.guild.id}"""
    
    result = db_conn(query1)

    # If the user does not exist in the database, insert them with default values.
    if result == []:
        query2 = f"""INSERT INTO levels (user_id, server_id, xp, level)
                    VALUES ({author.id}, {ctx.guild.id}, 0, 0)"""
        
        db_conn(query2, commit=True)
        result = db_conn(query1) 

    level = result[0][1]
    xp = result[0][0]

    # Calculate XP required for the next and previous levels.
    next_level_xp = ((int(level) + 1) / 0.1) ** 2
    next_level_xp = int(next_level_xp)
    previous_level_xp = ((int(level)) / 0.1) ** 2
    previous_level_xp = int(previous_level_xp)

    # Create a rank card using vacefron.
    rank_card = vacefron.Rankcard(
        username=author.display_name,
        avatar_url=author.avatar.url,
        level=level,
        current_xp=xp,
        next_level_xp=next_level_xp,
        previous_level_xp=previous_level_xp,
        background="default"
    )   

    client = vacefron.Client()
    try:
        card = await client.rankcard(rank_card)

        # Read the image data
        image_data = await card.read()

        # Create a BytesIO object from the image data
        image_bytes = io.BytesIO(image_data)

        # Create a discord.File object from the BytesIO object
        file = File(fp=image_bytes, filename="rank_card.png")
        
        await ctx.send(file=file)
    finally:
        await client.close()

async def handle_message(message):
    if message.author.bot:
        return
    
    # Query to get the user's XP and level from the database.
    query = f"""
    SELECT * FROM levels
    WHERE user_id = {message.author.id}
    AND server_id = {message.guild.id}
    """

    result = db_conn(query)

    # If the user does not exist in the database, insert them with default values.
    if result == []:
        query = f"""
        INSERT INTO levels (user_id, server_id, xp, level)
        VALUES ({message.author.id}, {message.guild.id}, 0, 0)
        """
        db_conn(query, commit=True)
    else:
        xp = result[0][2]
        level = result[0][3]
        xp_gained = random.randint(50, 51)
        xp += xp_gained
        new_lvl = math.floor(0.1 * math.sqrt(xp))

        # If the user has leveled up, update their level and XP in the database.
        if new_lvl > level:
            query = f"""
            UPDATE levels
            SET xp = {xp}, level = {new_lvl}
            WHERE user_id = {message.author.id}
            AND server_id = {message.guild.id}
            """
            db_conn(query, commit=True)

            role, prev_role = check_for_level_roles(message, new_lvl)

            if role is not None:
                try:
                    if prev_role is not None:
                        await message.author.remove_roles(prev_role)
                    await message.author.add_roles(role)
                except discord.errors.Forbidden:
                    await message.channel.send("Can't add or remove a role above my own role.")

                await message.channel.send(f"Congrats {message.author.mention}! You have leveled up to level {new_lvl} and received the role {role.mention}!")
            else:
                await message.channel.send(f"Congrats {message.author.mention}! You have leveled up to level {new_lvl}!")
        else:
            # If the user has not leveled up, just update their XP in the database.
            query = f"""
            UPDATE levels
            SET xp = {xp}
            WHERE user_id = {message.author.id}
            AND server_id = {message.guild.id}
            """
            db_conn(query, commit=True)

async def set_leveling_role(ctx, role, level):
    """The role will be mentioned in the command."""
    # Retrieve the id from the mentioned role
    role_id = role.id

    query = f"""
    INSERT INTO leveling_roles (server_id, role_id, level)
    VALUES ({ctx.guild.id}, {role_id}, {level})
    """

    db_conn(query, commit=True)

    await ctx.send(f"Role {role.mention} has been set as a leveling role for level **{level}**!!!")

def retrieve_level_roles(ctx):
    role_ids = {}
    guild_id = ctx.guild.id

    query = f"""SELECT role_id, level 
                FROM leveling_roles 
                WHERE server_id = {guild_id}"""

    results = db_conn(query)

    for result in results:
        role_id = result[0]
        level = result[1]
        role_ids[level] = role_id

    print(role_ids)
    return role_ids

def check_for_level_roles(ctx, new_level):
    role_ids = retrieve_level_roles(ctx)

    if not role_ids:
        return None, None
    if new_level in role_ids:
        role_id = role_ids[new_level]
        role = ctx.guild.get_role(role_id)
        
        # Get all keys that are less than the given key
        lower_levels = [k for k in role_ids.keys() if k < new_level]
        
        if not lower_levels:
            return role, None  # Return None if no lower level exists
        
        # Get the maximum of the lower levels
        closest_lower_level = max(lower_levels)
        
        # Return the value corresponding to the closest lower level
        prev_role_id = role_ids[closest_lower_level]    
        prev_role_id = ctx.guild.get_role(prev_role_id)

        return role, prev_role_id


def show_level_roles(ctx):
    role_ids = retrieve_level_roles(ctx)
    if not role_ids:
        return "No leveling roles have been set for this server."

    roles = []
    for level, role_id in role_ids.items():
        role = ctx.guild.get_role(role_id)
        roles.append(f"Level {level}: {role.mention}")

    return "\n".join(roles)
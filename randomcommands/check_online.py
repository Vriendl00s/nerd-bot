from moderationtools.moderation import check_admin
from standardutils.reply import reply
from db_connection import db_conn

async def register_online(ctx):
    """Register a channel to display the number of online users."""
    channel = await ctx.guild.create_text_channel('loading...')
    await channel.set_permissions(ctx.guild.default_role, read_messages=False)

    query = f"""
    INSERT INTO online_channel (guild_id, channel_id)
    VALUES ({ctx.guild.id}, {channel.id})
    """
    db_conn(query, commit=True)

    await reply(ctx, f"Registered {channel.mention} to display the number of online users.")
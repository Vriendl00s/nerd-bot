import discord
from botToken import token
from discord.ext import commands
from moderationtools import moderation
from discord import app_commands
from randomcommands.check_online import register_online
from randomcommands.remindme import remindme_save
from randomcommands.leveling import check_level, set_leveling_role

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('syncing commands...')
    # await bot.tree.sync()
    print('commands synced')
    print('loading cogs...')
    await bot.load_extension('cogs.background_tasks')
    await bot.load_extension('cogs.leveling')
    print('cogs loaded')
    print(f'We have logged in as {bot.user}')

@bot.tree.command(name="ban", description="Ban a user")
@app_commands.describe(user="The user to ban", length="The duration of the ban", reason="The reason for the ban")
async def slash_command(interaction: discord.Interaction, user: discord.User, length: str = None, reason: str = None):
    member = await interaction.guild.fetch_member(user.id)
    await moderation.ban(interaction, member, length, reason)

@bot.command()
async def ban(ctx, user: discord.User, length=None, reason=None):
    user = await ctx.guild.fetch_member(user.id)
    await moderation.ban(ctx, user, length, reason)

@bot.tree.command(name="unban", description="Unban a user")
@app_commands.describe(user_id="The user to unban")
async def slash_command(interaction: discord.Interaction, user_id: str):
    user = await bot.fetch_user(user_id)
    await moderation.unban(interaction, user)

@bot.command()
async def unban(ctx, user_id):
    user = await bot.fetch_user(user_id)
    await moderation.unban(ctx, user)

@bot.tree.command(name="kick", description="Kick a user")
@app_commands.describe(user="The user to kick", reason="The reason for the kick")
async def slash_command(interaction: discord.Interaction, user: discord.User, reason: str = None):
    member = await interaction.guild.fetch_member(user.id)
    await moderation.kick(interaction, member, reason)

@bot.command()
async def kick(ctx, user: discord.User, reason=None):
    user = await ctx.guild.fetch_member(user.id)
    await moderation.kick(ctx, user, reason)

@bot.tree.command(name="mute", description="Mute a user")
@app_commands.describe(user="The user to mute", length="The duration of the mute", reason="The reason for the mute")
async def slash_command(interaction: discord.Interaction, user: discord.User, length: str = None, reason: str = None):
    member = await interaction.guild.fetch_member(user.id)
    await moderation.mute(interaction, member, length, reason)

@bot.command()
async def mute(ctx, user: discord.User, length=None, reason=None):
    user = await ctx.guild.fetch_member(user.id)
    await moderation.mute(ctx, user, length, reason)

@bot.tree.command(name="unmute", description="Unmute a user")
@app_commands.describe(user="The user to unmute")
async def slash_command(interaction: discord.Interaction, user: discord.User):
    member = await interaction.guild.fetch_member(user.id)
    await moderation.unmute(interaction, member)


@bot.command()
async def unmute(ctx, user: discord.User):
    user = await ctx.guild.fetch_member(user.id)
    await moderation.unmute(ctx, user)

@bot.tree.command(name="warn", description="Warn a user")
@app_commands.describe(user="The user to warn", reason="The reason for the warn")
async def slash_command(interaction: discord.Interaction, user: discord.User, reason: str = None):
    member = await interaction.guild.fetch_member(user.id)
    await moderation.warn(interaction, member, reason)

@bot.command()
async def warn(ctx, user: discord.User, reason=None):
    user = await ctx.guild.fetch_member(user.id)
    await moderation.warn(ctx, user, reason)

@bot.tree.command(name="clear", description="Clear messages")
@app_commands.describe(amount="The amount of messages to clear")
async def slash_command(interaction: discord.Interaction, amount: int = 5):
    await moderation.clear(interaction, amount)

@bot.command()
async def clear(ctx, amount=5):
    await moderation.clear(ctx, amount)

@bot.tree.command(name="check_online", description="Makes a channel to display the number of online users")
async def slash_command(interaction: discord.Interaction):
    await register_online(interaction)

@bot.command()
async def check_online(ctx):
    await register_online(ctx)

@bot.tree.command(name="remindme", description="Remind me")
@app_commands.describe(message="The message to remind you", time_until="The time until the reminder")
async def slash_command(interaction: discord.Interaction, message: str, time_until: str):
    await remindme_save(interaction, message, time_until)

@bot.command()
async def remindme(ctx, message, time_until):
    await remindme_save(ctx, message, time_until)

@bot.tree.command(name="level", description="Check your level")
async def slash_command(interaction: discord.Interaction):
    await check_level(interaction)

@bot.command()
async def level(ctx):
    await check_level(ctx)

@bot.tree.command(name="level_role_add", description="Add a role to a level")
@app_commands.describe(role="Mentions the role to add", level="The level to add the role to")
async def slash_command(interaction: discord.Interaction, role: discord.Role, level: int):
    await set_leveling_role(interaction, role, level)

@bot.command()
async def level_role_add(ctx, role: discord.Role, level: int):
    await set_leveling_role(ctx, role, level)

bot.run(token)
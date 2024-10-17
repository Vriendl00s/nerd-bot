import discord

async def reply(ctx, message):
    try:
        return await ctx.reply(message)
    except AttributeError:
        try:
            return await ctx.response.send_message(message)
        except discord.InteractionResponded:
            return await ctx.followup.send(message)
        
async def reply_file(ctx, file):
    try:
        return await ctx.reply(file=file)
    except AttributeError:
        try:
            return await ctx.response.send_message(file=file)
        except discord.InteractionResponded:
            return await ctx.followup.send(file=file)
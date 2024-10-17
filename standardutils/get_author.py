async def get_author(ctx):
    """Get the author of the message."""
    try:
        return ctx.author
    except AttributeError:
        return ctx.user
import typing
import discord
from discord.ext import commands

# works with python 3.6+ I think

TOKEN = "INSERT BOT TOKEN HERE"
PREFIXES = ["peachy is gay ", "lalamilk ", "why though "]


class Lalacon(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# since I have a say command and in the future may implement replies for long to process commands
allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, replied_user=False)
intents = discord.Intents.default()  # All but the privileged ones

bot = Lalacon(command_prefix=commands.when_mentioned_or(*PREFIXES),
              case_insensitive=True,
              intents=intents,
              allowed_mentions=allowed_mentions)


@bot.event
async def on_ready():
    print(f"Successfully logged in and booted...!")
    print(f"\nLogged in as: {bot.user.name} - {bot.user.id}\nDiscord.py version: {discord.__version__}\n")


@bot.command()
async def source(ctx):
    """
    returns the bot github url
    -------------------------------------------------------------
    lalamilk source
    """
    await ctx.send("https://github.com/CaladBlogBaal/Tataru")


@bot.command()
async def say(ctx, *, mesasage):
    """
    Echo a message
    -------------------------------------------------------------
    lalamilk say message
    """
    await ctx.send(mesasage)


@bot.command()
async def ping(ctx):
    """
    Returns the bots web socket latency
    -------------------------------------------------------------
    lalamilk ping
    """

    await ctx.send(f":information_source: | :ping_pong: **{ctx.bot.latency * 1000:.0f}**ms")


@bot.command()
async def prefix(ctx):
    """
    returns the bot current prefixes
    -------------------------------------------------------------
    lalamilk prefix
    """
    await ctx.send(f"The prefixes for this bot is {ctx.prefix}")


@bot.command()
async def invite(ctx):
    """
    returns the bot invite url
    -------------------------------------------------------------
    lalamilk invite
    """
    await ctx.send(discord.utils.oauth_url(ctx.me.id, discord.Permissions(18496)))


@bot.command()
async def rename(ctx, new_name, channels: commands.Greedy[typing.Union[discord.TextChannel,
                                                                       discord.VoiceChannel,
                                                                       discord.StageChannel]]):
    """renames text/voice/stage channels with an inputted name in the order they're listed.
    -------------------------------------------------------------
    lalamilk "deez nutz" #general #memes
    lalamilk "deez nutz" 601128182363586560 565505126668697600
    lalamilk "deez nutz" general memes
    """

    inputted_channels = channels

    if any(channel.name == new_name for channel in inputted_channels):
        return await ctx.send(f"One of the channel(s) inputted is already named `{new_name}`")

    if not inputted_channels:
        return await ctx.send("A valid channel(s) wasn't given.")

    for channel in inputted_channels:
        await channel.edit(name=new_name)

    channels = ctx.guild.channels

    get_edited_channels = [channel for channel in channels
                           if channel.type in (
                               discord.ChannelType.text,
                               discord.ChannelType.stage_voice,
                               discord.ChannelType.voice)
                           and channel.name == new_name]

    if len(get_edited_channels) == len(inputted_channels):
        return await ctx.send(f"Edited all text/voice/stage channel(s) with the new name `{new_name}`.")

    await ctx.send(f"Renaming all channel(s), with `{new_name}` failed, probably due to ratelimits "
                   f"(2 channel edits per 10 mins.)")


@rename.error
async def rename_error(ctx, error):

    if isinstance(error, discord.ext.commands.errors.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.MissingPermissions) or isinstance(error, discord.Forbidden):
        return await ctx.send("Missing manage channel permissions to run this command.")

    await ctx.send(f"The command `{ctx.command.name}` has ran into an unexpected error contact the bot's owner.",
                   delete_after=8)

    raise error


if __name__ == "__main__":
    bot.run(TOKEN, bot=True, reconnect=True)

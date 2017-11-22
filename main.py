import atexit
import logging
import discord
from discord.ext import commands
from dahandler import Dahandler

logging.basicConfig(level=logging.DEBUG)

class DeviantBot:
    """ Bot that prints random deviation from deviantArt """

    def __init__(self, bot):
        self.bot = bot
        self.dah = Dahandler()

    @commands.command(no_pm=True, pass_context=True)
    async def darand(self, context):
        """ Print random deviation """

        deviation = await self.dah.getrandomdeviation()
        avatar = await self.dah.getuserinfo(deviation["url"])

        embed = discord.Embed(title=deviation["url"], colour=discord.Colour(0x6ffafc), url=deviation["url"], description=deviation["desc"])

        embed.set_image(url=deviation["img"])
        embed.set_thumbnail(url=avatar["avatar_url"])
        embed.set_author(name=avatar["name"], url=avatar["url"])

        await self.bot.send_message(context.message.channel, embed=embed)
        return

    async def cleanup(self):
        """ Clean everything """
        self.dah.cleanup()
        return


atexit.register(DeviantBot.cleanup)

BOT = commands.Bot(command_prefix=commands.when_mentioned_or("$"))
BOT.add_cog(DeviantBot(BOT))

# Put your bot token here
BOT.run('token')

@BOT.event
async def on_ready():
    """ Excute update status and username when ready"""
    await BOT.edit_profile(username="DeviantBot")
    await BOT.change_presence(game=discord.Game(name="$dahelp"))

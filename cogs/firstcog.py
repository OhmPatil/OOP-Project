from discord.ext import commands
import discord
import time


class TestCogCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """Get the bot's current websocket and API latency."""
        start_time = time.time()
        message = await ctx.reply("Testing Ping...")
        end_time = time.time()

        await message.edit(
            content=f"Pong! {round(self.bot.latency * 1000)}ms\nAPI: {round((end_time - start_time) * 1000)}ms")

    @commands.command(name="setstatus")
    async def set_status(self, ctx: commands.Context, *, text: str):
        await self.bot.change_presence(activity=discord.Game(name=text))

    @commands.command(name="snipeback")
    async def snipe(self, ctx: commands.Context):
        """A command to snipe delete messages."""
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author
        content = self.last_msg.content

        embed = discord.Embed(title=f"Message from {author}", description=content)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(857609403703361547)

        if not channel:
            return

        await channel.send(f"Welcome, {member}!")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.command(name="afk")
    async def afk(self, ctx, *, message="They didn't leave a message!"):
        if ctx.message.author in self.bot.afkdict:
            self.bot.afkdict.pop(ctx.message.author)
            await ctx.send('Welcome back! You are no longer afk.')
        else:
            self.bot.afkdict[ctx.message.author] = message
            await ctx.send("You are now afk. Beware of the real world!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return

        for member in message.mentions:
            if member != message.author and member in self.bot.afkdict:
                await message.reply(
                    content=f"Oh noes! {member.mention} is currently AFK.\nReason: **{self.bot.afkdict[member]}**",
                    delete_after=20)


def setup(bot: commands.Bot):
    bot.add_cog(TestCogCommands(bot))

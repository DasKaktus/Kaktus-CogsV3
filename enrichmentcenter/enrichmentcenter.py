from datetime import datetime
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core import Config

defaults = {"UserProgress": []}
# "873584735": {"stage": "1", "started": "2020-07-25 01:00:15", "lastfinished": "2020-07-15 11:04:39"}

class EnrichmentCenter(commands.Cog):
    """EnrichmentCenter Cog"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784274, force_registration=True)
        self.config.register_guild(**defaults)
        self.players = []

    @commands.command()
    async def sendMsgToChannel(self, ctx, *, message):
        channel = ctx.channel
        await channel.send(message)
        
    @commands.command()
    async def dmPerson(self, ctx, *, message):
        author = ctx.author
        await author.send(message)
        
    @commands.command()
    async def sendFileImage(self, ctx):
        my_files = [
            discord.File('file_path.png', 'filename.png'),
            discord.File('other_file_path.png', 'other_filename.png')
        ]
        await ctx.send('Images:', files=my_files)
        
    @commands.command()
    async def sendCodeBlock(self, ctx, *, message):
        await ctx.send(box(message))
        
    @commands.command()
    async def sendCodeBlockWithColor(self, ctx):
        message = "Ruby will Highlight words that are Capitalized."
        await ctx.send(box(message, lang='ruby'))
        
    @commands.command()
    async def getUserInfo(self, ctx, member: discord.Member):
        author_name = ctx.author.name
        author_id = ctx.author.id
        member_name = member.name
        member_id = member.id
        await ctx.send(f'Author Name: {author_name}\nAuthor ID: {author_id}\n'
                       f'Member Name: {member_name}\nMember ID: {member_id}')
                       
    @commands.command()
    async def sendEmbed(self, ctx):
        embed = discord.Embed(color=0xEE2222, title='New Embed')
        embed.add_field(name='title 1', value='value 1')
        embed.add_field(name='title 2', value='value 2')
        embed.set_footer(text='I am the footer!')   
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def cooldownCommand(self, ctx):
        await ctx.send("I can only be used once every 30 seconds, per user")







    @commands.command()
    async def allEnrichment(self, ctx):
        data = await self.config.guild(ctx.guild).all()
        await ctx.send(data)
        
    @commands.command()
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def whichStage(self, ctx):
        user = ctx.author
        settings = await self.config.guild(ctx.guild).all()
        usrprogress = self.config.guild(ctx.guild).UserProgress()
        foot = "Total amount of subjects: {}".format(len(settings["UserProgress"]))
        embed = discord.Embed(color=0xEE2222, title='User Progress')
        embed.add_field(name='Stage', value=usrprogress[user.id].stage)
        embed.add_field(name='Last stage finished', value=usrprogress[user.id].lastfinished)
        embed.set_footer(text=foot)   
        await ctx.send(embed=embed)

    @commands.command()
    async def startEnrichment(self, ctx):
        user = ctx.author
        channel = ctx.channel
        settings = await self.config.guild(ctx.guild).all()

        if user.id in settings["UserProgress"]:
            pass
        else:
            timenow = datetime.now()
            now = timenow.strftime("%Y-%m-%d %H:%M:%S")
            userinfo = {user.id: {"stage": 1, "started": now, "lastfinished": "0000-00-00 00:00:00"}}
            async with self.config.guild(ctx.guild).UserProgress() as users:
                users.append(userinfo)
            
    
from datetime import datetime
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core import Config

class commandException(Exception):
    pass
    
class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args:
            self.fall = True
            return True
        else:
            return False

class EnrichmentCenter(commands.Cog):
    """EnrichmentCenter Cog"""
    
    default_member = {"stage": 0, "started": "0000-00-00 00:00:00", "lastfinished": "0000-00-00 00:00:00"}
    
    helptext = """Aperture Science Personnel File; #{author.id}

Test Subject Name; {author.name}

Status; Alive

----------------------------------------------------

Hello and welcome to the Aperture Science computer-aided enrichment center. The enrichment center consists of multiple chambers designed to challenge your puzzle solving skills, knowledge of cryptography and ability to find hidden messages. 

To complete each chamber you must discover the command hidden within the puzzle to progress to the next chamber and receive the next puzzle. 

All commands use the same basic format of "!Aperture-Science-" followed by a code/text string unique to that puzzle which is used to access the next puzzle.

These puzzles use a variety of techniques from simple ciphers to more challenging methods of hiding messages.

Good luck.

— Doug-Rattmann"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784274, force_registration=True)
        self.config.register_member(**self.default_member)
        #self.players = []
        
        
    @commands.command()
    #@commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def whichStage(self, ctx):
        user = ctx.author
        member_settings = self.config.member(user)
        curr_stage = await member_settings.stage()
        curr_lastfinish = await member_settings.lastfinished()
        embed = discord.Embed(color=0xEE2222, title='Testsubject report card')
        if curr_stage == 0:
            embed.add_field(name='Stage', value="N/A")
        else:
            embed.add_field(name='Stage', value=curr_stage)
        if curr_lastfinish == "0000-00-00 00:00:00":
            embed.add_field(name='Last stage finished', value="N/A")
        else:
            embed.add_field(name='Last stage finished', value=curr_lastfinish)
        embed.set_footer(text="Enrichmentcenter")
        await ctx.send(embed=embed)
        
    @commands.command()
    async def startEnrichment(self, ctx):
        user = ctx.author
        channel = ctx.channel
        member_settings = self.config.member(user)
        await member_settings.stage.set(1)

    @commands.Cog.listener()
    async def on_message_without_command(self, message):
        ctx = await self.bot.get_context(message)
        user_allowed = True
        is_private = isinstance(message.channel, discord.abc.PrivateChannel)
        if len(message.content) < 2 or is_private or not user_allowed or message.author.bot:
            return
        
        if ctx.prefix is None:
            return
        
        try:
            cclower = ctx.invoked_with.lower()
        except commandException:
            return
        
        cclower
        for case in switch(cclower):
            if case('aperture-science-help'):
                sendCodeBlock(ctx, "http", helptext)
                break
            if case('aperture-science-initiate'):
                print 2
                break
            if case('aperture-science-c-uhswhbcjh-'):
                print 10
                break
            if case('aperture-science-c-dgwrgdfg-'):
                print 11
                break
     
        
    async def sendCodeBlock(self, ctx, language: str, msg: string):
        msg = msg.replace("{author.id}", ctx.author.id) 
        msg = msg.replace("{author.name}", ctx.author.name) 
        await ctx.send(box(msg, lang=language))    
        
        

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
    async def ccv(self, ctx):
        data = await self.config.guild(ctx.guild).userprogress()
        await ctx.send(data[ctx.author.id])
        
    @commands.command()
    async def allEnrichment(self, ctx):
        data = await self.config.guild(ctx.guild).all()
        await ctx.send(data)
        

    
            
    @commands.command()  
    async def clearCenter(self, ctx):  
        await self.config.guild(ctx.guild).clear()
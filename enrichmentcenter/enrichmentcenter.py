from datetime import datetime
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core import Config



class EnrichmentCenter(commands.Cog):
    """EnrichmentCenter Cog"""
    
    default_member = {"stage": 0, "started": "0000-00-00 00:00:00", "lastfinished": "0000-00-00 00:00:00"}
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784274, force_registration=True)
        self.config.register_member(**self.default_member)
        #self.players = []
        
        
    @commands.command()
    @commands.cooldown(rate=1, per=30, type=commands.BucketType.user)
    async def whichStage(self, ctx):
        user = ctx.author
        member_settings = self.config.member(user)
        foot = "Total amount of subjects: {}".format(len(self.config.member()))
        embed = discord.Embed(color=0xEE2222, title='User Progress')
        if member_settings["stage"] == 0:
            embed.add_field(name='Stage', value="N/A")
            embed.add_field(name='Last stage finished', value="N/A")
        else:
            embed.add_field(name='Stage', value=member_settings["stage"])
            embed.add_field(name='Last stage finished', value=member_settings["lastfinished"])
        embed.set_footer(text=foot)   
        await ctx.send(embed=embed)
        
    @commands.command()
    async def startEnrichment(self, ctx):
        user = ctx.author
        channel = ctx.channel
        member_settings = self.config.member(user)
        member_settings.stage.set(1)

   
        
        
        
        
        
        
        
        
        

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
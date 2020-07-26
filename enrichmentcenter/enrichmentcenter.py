from datetime import datetime
import asyncio
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core import Config
from discord.ext import tasks

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

    stage1 = """Aperture Science Personnel File; #{author.id}

Test Subject Name; {author.name}

Status; Alive

----------------------------------------------------

Hello and, again, welcome to the Aperture Science computer-aided enrichment center. We hope your brief detention in the relaxation vault has been a pleasant one. Your specimen has been processed and we are now ready to begin the test proper. Before we start, however, keep in mind that, although fun and learning are the primary goals of all enrichment center activities, serious injuries may occur. For your own safety, and the safety of others, please refrain from — *static* Por favor bordón de fallar Muchos gracias de fallar gracias *static* Stand back. The portal will open in 3, 2, 1...``` ```diff
-HJCBHWSHU-C-ecneicS-erutrepA! .ebuC egarotS dethgieW ecneicS erutrepA eht ,ecnatsni rof - ti hguorht sessap taht tnempiuqe dezirohtuanu yna eziropav lliw llirG noitapicnamE lairetaM ecneicS erutrepA sihT .tixe eht ssorca dleif elcitrap tnecsednacni eht eton ,revewoh ,tsriF .tset hcae gnitelpmoc retfa kcolrebmahc eht otni deecorp esaelP .tnellecxE-"""
    
    stage2 = """Aperture Science Personnel File; #{author.id}

Test Subject Name; {author.name}

Status; Alive

----------------------------------------------------

You're doing very well. Please be advised that a noticeable taste of blood is not part of any test protocol but is an unintended side effect of the Aperture Science Material Emancipation Grill, which may, in semi-rare cases, emancipate dental fillings, crowns, tooth enamel, and teeth.``` ```diff
-https://discordapp.com/channels/239788202745921536/239788202745921536/436554881252196354-"""

    stage3_1 = """Aperture Science Personnel File; #{author.id}

Test Subject Name; {author.name}

Status; Alive

----------------------------------------------------

Please proceed to the chamberlock. >_________________> . Mind the gap."""

    stage3_2 = """-Fnuu mxwn. Anvnvkna, cqn Jynacdan Blrnwln Karwp Hxda Mjdpqcna cx Fxat Mjh rb cqn ynaonlc crvn cx qjen qna cnbcnm. !Jynacdan-Blrnwln-L-OBMOBFNOB-"""
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784274, force_registration=True)
        self.config.register_member(**self.default_member)
        self.messageids = []
        #self.msgupdater = self.bot.loop.create_task(self.selfDestructMessage2())
        self.selfDestructMessage.start()
    
    def cog_unload(self):
        self.selfDestructMessage.cancel()
        
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
        embed.set_footer(text="This message will selfdestruct in 30 seconds")
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
        
        for case in switch(cclower):
            if case('aperture-science-help'):
                await self.sendCodeBlock(ctx, "http", self.helptext)
                break
            if case('aperture-science-initiate'):
                await self.sendCodeBlock(ctx, "http", self.stage1)
                break
            if case('aperture-science-c-uhswhbcjh-'):
                await self.sendCodeBlock2(ctx, "http", self.stage2)
                break
            if case('aperture-science-c-dgwrgdfg-'):
                await self.sendCodeBlock(ctx, "http", self.stage3_1)
                await self.sendCodeBlock(ctx, "diff", self.stage3_2)
                break
     
        
    async def sendCodeBlock(self, ctx, language: str, msg: str):
        msg = msg.replace("{author.id}", str(ctx.author.id)) 
        msg = msg.replace("{author.name}", str(ctx.author.name)) 
        sendit = await ctx.send(box(msg, lang=language))
        
        # Add sendit.id to an list with an endtime.
        # A timer that checks if message should be deleted?
        self.messageids.append(sendit.id)
    
    async def sendCodeBlock2(self, ctx, language: str, msg: str):
        msg = msg.replace("{author.id}", str(ctx.author.id)) 
        msg = msg.replace("{author.name}", str(ctx.author.name))
        embed = discord.Embed(color=0xEE2222, title='Test')
        embed.add_field(name='Computer output', value=box(msg, lang=language))
        embed.set_footer(text="This message will selfdestruct in: 30 seconds")
        sendit = await ctx.send(embed=embed)
        #sendit = await ctx.send(box(msg, lang=language))
        
        # Add sendit.id to an list with an endtime.
        # A timer that checks if message should be deleted?
        self.messageids.append(sendit.id)
        #await self.selfDestructMessage(ctx)
        
    #async def selfDestructMessage(self, ctx):
    #    await asyncio.sleep(1)
    #    for msgid in self.messageids:
    #        try:
    #            message = await ctx.channel.get_message(msgid)
    #        except AttributeError:
    #            message = await ctx.channel.fetch_message(msgid)
    #        
    #        org_msg = message.embeds[0].fields[0].value
    #        
    #        
    #        tid = int(message.embeds[0].footer.text.split(":")[1].split()[0])
    #        tid = tid - 1
    #        
    #        newembed = discord.Embed(color=0xEE2222, title='Test')
    #        newembed.add_field(name='Computer output', value=org_msg)
    #        newembed.set_footer(text="This message will selfdestruct in: {} seconds".format(tid))
    #        await message.edit(embed=newembed)

    @tasks.loop(seconds=1.0)
    async def selfDestructMessage(self):
        #await asyncio.sleep(1)
        await ctx.send("loop")
        for msgid in self.messageids:
            try:
                message = await ctx.channel.get_message(msgid)
            except AttributeError:
                message = await ctx.channel.fetch_message(msgid)
            
            org_msg = message.embeds[0].fields[0].value
            
            
            tid = int(message.embeds[0].footer.text.split(":")[1].split()[0])
            tid = tid - 1
            
            newembed = discord.Embed(color=0xEE2222, title='Test')
            newembed.add_field(name='Computer output', value=org_msg)
            newembed.set_footer(text="This message will selfdestruct in: {} seconds".format(tid))
            await message.edit(embed=newembed)
                
    @selfDestructMessage.before_loop
    async def before_selfdestruct(self):            
        await self.bot.wait_until_ready()
                
                
                
                
                
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
        
    #@commands.command()
    #async def sendCodeBlock(self, ctx, *, message):
    #    await ctx.send(box(message))
        
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
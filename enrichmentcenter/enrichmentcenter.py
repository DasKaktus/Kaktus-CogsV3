from datetime import datetime
import asyncio
import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import box
from redbot.core import Config
from discord.ext import tasks

# Puzzles
import .helptext
import .stage1
import .stage2
import .stage3

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
    
    default_guild = {"wlchannels": [], "whitelist": True }
    
    selfdestructtimer = 30
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784274, force_registration=True)
        self.config.register_member(**self.default_member)
        self.data.register_guild(**default_guild)
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
        embed.set_footer(text="This message will selfdestruct in {} seconds".format(selfdestructtimer))
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
        try:
            await message.delete()
        except Exception:
            pass
        for case in switch(cclower):
            if case('aperture-science-help'):
                await self.sendCodeBlock(ctx, "http", helptext.text1)
                break
            if case('aperture-science-initiate'):
                await self.sendCodeBlock(ctx, "http", stage1.text1)
                break
            if case('aperture-science-c-uhswhbcjh-'):
                await self.sendCodeBlock(ctx, "http", stage2.text1)
                break
            if case('aperture-science-c-dgwrgdfg-'):
                await self.sendCodeBlock(ctx, "http", stage3.text1)
                await self.sendCodeBlock(ctx, "diff", stage3.text2)
                break
    
    async def sendCodeBlock(self, ctx, language: str, msg: str):
        msg = msg.replace("{author.id}", str(ctx.author.id)) 
        msg = msg.replace("{author.name}", str(ctx.author.name))
        embed = discord.Embed(color=0xEE2222, title='Test')
        embed.add_field(name='Computer output', value=box(msg, lang=language))
        embed.set_footer(text="This message will selfdestruct in: {} seconds".format(selfdestructtimer))
        sendit = await ctx.send(embed=embed)
        self.messageids.append(sendit.id)
        self.ctx = ctx


    @tasks.loop(seconds=1.0)
    async def selfDestructMessage(self):
        if hasattr(self, 'ctx'):
            for msgid in self.messageids:
                try:
                    message = await self.ctx.channel.get_message(msgid)
                except AttributeError:
                    message = await self.ctx.channel.fetch_message(msgid)
                
                org_msg = message.embeds[0].fields[0].value
                
                
                tid = int(message.embeds[0].footer.text.split(":")[1].split()[0])
                tid = tid - 1
                
                if tid == 0:
                    try:
                        await message.delete()
                    except Exception:
                        pass
                    self.messageids.remove(msgid)
                else:
                    newembed = discord.Embed(color=0xEE2222, title='Test')
                    newembed.add_field(name='Computer output', value=org_msg)
                    newembed.set_footer(text="This message will selfdestruct in: {} seconds".format(tid))
                    await message.edit(embed=newembed)
                    
                
    @selfDestructMessage.before_loop
    async def before_selfdestruct(self):            
        await self.bot.wait_until_ready()
                
                
    async def _get_guild_channels(self, guild):
        return await self.data.guild(guild).wlchannels()
        
    async def _add_guild_channel(self, guild, channel):
        async with self.data.guild(guild).wlchannels() as chanlist:
            chanlist.append(channel)
            
    async def _toggle_whitelist(self, guild):
        wl = await self.data.guild(guild).whitelist()
        if wl:
            await self.data.guild(guild).whitelist.set(False)
            return False
        else:
            await self.data.guild(guild).whitelist.set(True)
            return True
            
    async def _remove_guild_channel(self, guild, channel):
        async with self.data.guild(guild).wlchannels() as chanlist:
            chanlist.remove(channel)

    @commands.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def enrichmentcenter(self, ctx):
        """Configuration commands."""
        pass
    
    @enrichmentcenter.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def channel(self, ctx):
        """Configure channels whitelist."""
        pass
        
    @channel.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def whitelist(self, ctx):
        """Whitelist configuration."""
        pass
        
    @whitelist.command(name="add")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _add(self, ctx, channel: discord.TextChannel = None):
        """Add a channel to the whitelist."""
        if channel is None:
            channel = ctx.channel
        if channel.id not in await self._get_guild_channels(ctx.guild):
            await self._add_guild_channel(ctx.guild, channel.id)
            await ctx.send(_("Channel added"))
        else:
            await ctx.send(_("Channel already whitelisted"))
            
    @whitelist.command(name="toggle")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def toggle(self, ctx):
        """Toggle whitelist on/off."""
        new = await self._toggle_whitelist(ctx.guild)
        verb = _("activated.") if new else _("deactivated.")
        await ctx.send(_("Whitelist is {verb}").format(verb=verb))

    @whitelist.command(name="remove")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _remove(self, ctx, channel: discord.TextChannel = None):
        """Delete a channel from the whitelist."""
        if channel is None:
            channel = ctx.channel
        if channel.id not in await self._get_guild_channels(ctx.guild):
            await ctx.send(_("This channel isn't whitelisted."))
        else:
            await self._remove_guild_channel(ctx.guild, channel.id)
            await ctx.send(_("Channel deleted"))

    @whitelist.command(name="show")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _show(self, ctx):
        """Show the list of channels configured to allow earning experience."""
        emb = discord.Embed()
        emb.title = _("List of channels configured to allow enrichment commands.")
        emb.description = _("All things in the world aren't round therre is red objects too")
        channels = await self._get_guild_channels(ctx.guild)
        if not len(channels):
            return await ctx.send(_("No channels configured"))
        emb.add_field(
            name="Channels:", value="\n".join([ctx.guild.get_channel(x).mention for x in channels])
        )
        await ctx.send(embed=emb)





















                
                
                
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
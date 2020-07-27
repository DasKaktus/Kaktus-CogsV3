from datetime import datetime
import asyncio
import discord
from redbot.core import commands, checks, Config
from redbot.core.utils.chat_formatting import box
from discord.ext import tasks

# Puzzles
from .helptext import Helptext
from .stage1 import Stage1
from .stage2 import Stage2
from .stage3 import Stage3
from .stage4 import Stage4
from .stage5 import Stage5
from .stage6 import Stage6
from .stage7 import Stage7
from .stage8 import Stage8
from .stage9 import Stage9
from .stage10 import Stage10
from .stage11 import Stage11
from .stage12 import Stage12
from .stage13 import Stage13
from .stage14 import Stage14
from .stage15 import Stage15
from .stage16 import Stage16
from .stage17 import Stage17
from .stage18 import Stage18
from .stage19 import Stage19
from .stage20 import Stage20
from .stage21 import Stage21
from .stage22 import Stage22
from .stage23 import Stage23
from .stage24 import Stage24
from .stage25 import Stage25
from .stage26 import Stage26
from .stage27 import Stage27
from .stage28 import Stage28
from .stage29 import Stage29
from .stage30 import Stage30


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
    
    default_member = {"stage": 0, "started": "0000-00-00 00:00:00", "stagefinished": {1: "0000-00-00 00:00:00", 2: "0000-00-00 00:00:00", 3: "0000-00-00 00:00:00", 4: "0000-00-00 00:00:00", 5: "0000-00-00 00:00:00", 6: "0000-00-00 00:00:00", 7: "0000-00-00 00:00:00", 8: "0000-00-00 00:00:00", 9: "0000-00-00 00:00:00", 10: "0000-00-00 00:00:00", 11: "0000-00-00 00:00:00", 12: "0000-00-00 00:00:00", 13: "0000-00-00 00:00:00", 14: "0000-00-00 00:00:00", 15: "0000-00-00 00:00:00", 16: "0000-00-00 00:00:00", 17: "0000-00-00 00:00:00", 18: "0000-00-00 00:00:00", 19: "0000-00-00 00:00:00", 20: "0000-00-00 00:00:00", 21: "0000-00-00 00:00:00", 22: "0000-00-00 00:00:00", 23: "0000-00-00 00:00:00", 24: "0000-00-00 00:00:00", 25: "0000-00-00 00:00:00", 26: "0000-00-00 00:00:00", 27: "0000-00-00 00:00:00", 28: "0000-00-00 00:00:00", 29: "0000-00-00 00:00:00", 30: "0000-00-00 00:00:00"}}
    
    default_guild = {"wlchannels": [], "whitelist": True }
    
    selfdestructtimer = 30
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784274133784274, force_registration=True)
        self.config.register_member(**self.default_member)
        self.config.register_guild(**self.default_guild)
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
        embed.set_footer(text="This message will selfdestruct in {} seconds".format(self.selfdestructtimer))
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
        
        if await self.config.guild(message.guild).whitelist():
            if message.channel.id not in await self._get_guild_channels(message.author.guild):
                return
        
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
                await self.sendCodeBlock(ctx, "http", Helptext.text1)
                break
            if case('aperture-science-initiate'):
                
                await self.sendCodeBlock(ctx, "http", Stage1.text1)
                await self.sendCodeBlock(ctx, "diff", Stage1.text2)
                break
            if case('aperture-science-c-uhswhbcjh-'):
                self.userProgress(2, message.author)
                await self.sendCodeBlock(ctx, "http", Stage2.text1)
                await self.sendCodeBlock(ctx, "diff", Stage2.text2)
                break
            if case('aperture-science-c-dgwrgdfg-'):
                await self.sendCodeBlock(ctx, "http", Stage3.text1)
                await self.sendCodeBlock(ctx, "diff", Stage3.text2)
                break
            if case('aperture-science-c-fsdfswefs-'):
                await self.sendCodeBlock(ctx, "http", Stage4.text1)
                await self.sendCodeBlock(ctx, "diff", Stage4.text2)
                break;
            if case('aperture-science-c-xdergwerg-'):
                await self.sendCodeBlock(ctx, "diff", Stage5.text1)
                break;
            if case('aperture-science-c-gsresdfgd-'):
                await self.sendCodeBlock(ctx, "http", Stage6.text1)
                await self.sendCodeBlock(ctx, "diff", Stage6.text2)
                break;
            if case('aperture-science-c-pfiejchen-'):
                await self.sendCodeBlock(ctx, "http", Stage7.text1)
                await self.sendCodeBlock(ctx, "diff", Stage7.text2)
                break;
            if case('aperture-science-c-fayhsdbfg-'):
                await self.sendCodeBlock(ctx, "http", Stage8.text1)
                await self.sendCodeBlock(ctx, "diff", Stage8.text2)
                break;
            if case('aperture-science-c-hiauhdiua-'):
                await self.sendCodeBlock(ctx, "diff", Stage9.text1)
                break;
            if case('aperture-science-c-safhsiuhf-'):
                await self.sendCodeBlock(ctx, "http", Stage10.text1)
                await self.sendCodeBlock(ctx, "diff", Stage10.text2)
                break;
            if case('aperture-science-c-oudfhaiuh-'):
                await self.sendCodeBlock(ctx, "http", Stage11.text1)
                await self.sendCodeBlock(ctx, "fix", Stage11.text2)
                break;
            if case('aperture-science-c-sujdbisud-'):
                await self.sendCodeBlock(ctx, "http", Stage12.text1) #### TEST this, weird characters
                await self.sendCodeBlock(ctx, "diff", Stage12.text2)
                break;
            if case('aperture-science-c-asijsihug-'):
                await self.sendCodeBlock(ctx, "http", Stage13.text1)
                await self.sendCodeBlock(ctx, "diff", Stage13.text2)
                break;
            if case('aperture-science-c-udjfhbaiu-'):
                await self.sendCodeBlock(ctx, "http", Stage14.text1) #### Kolla alla innan efter flera texter
                break;
            if case('aperture-science-incinerate_faithful_companion_cube'):
                await self.sendCodeBlock(ctx, "http", Stage15.text1)
                await self.sendCodeBlock(ctx, "diff", Stage15.text2)
                await self.sendCodeBlock(ctx, "diff", Stage15.text3)
                break;
            if case('aperture-science-c-oeisoijfh-'):
                await self.sendCodeBlock(ctx, "http", Stage16.text1)
                await self.sendCodeBlock(ctx, "diff", Stage16.text2)
                break;
            if case('aperture-science-cake-whoah-yeah-cccccccake-'):
                await self.sendCodeBlock(ctx, "diff", Stage17.text1)
                break;
            if case('aperture-science-c-jhfbishjg-goodbye-'):
                await self.sendCodeBlock(ctx, "diff", Stage18.text1)
                await self.sendCodeBlock(ctx, "diff", Stage18.text2)
                break;
            if case('aperture-science-escape_glados_c-oiufhiuhi-'):
                await self.sendCodeBlock(ctx, "http", Stage19.text1)
                await self.sendCodeBlock(ctx, "diff", Stage19.text2)
                await self.sendCodeBlock(ctx, "diff", Stage19.text3)
                break;
            if case('aaperture-science-escape_glados_c-dahdgbuyh-'):
                await self.sendCodeBlock(ctx, "http", Stage20.text1)
                await self.sendCodeBlock(ctx, "diff", Stage20.text2)
                break;
            if case('aperture-science-confront-glados-central-ai-chamber-'):
                await self.sendCodeBlock(ctx, "http", Stage21.text1)
                await self.sendCodeBlock(ctx, "diff", Stage21.text2)
                await self.sendCodeBlock(ctx, "http", Stage21.text3)
                await self.sendCodeBlock(ctx, "diff", Stage21.text4)
                break;
            if case('aperture-science-glados-morality_core-jhfgbiuyd-'):
                await self.sendCodeBlock(ctx, "http", Stage22.text1)
                await self.sendCodeBlock(ctx, "diff", Stage22.text2)
                break;
            if case('aperture-science-destroy_morality_core_c-caijhiujd-'):
                await self.sendCodeBlock(ctx, "http", Stage23.text1)
                await self.sendCodeBlock(ctx, "diff", Stage23.text2)
                await self.sendCodeBlock(ctx, "http", Stage23.text3)
                break;
            if case('aperture-science-glados-curiosity-core-wockdjehc-'):
                await self.sendCodeBlock(ctx, "diff", Stage24.text1)
                await self.sendCodeBlock(ctx, "fix", Stage24.text2)
                break;
            if case('aperture-science-destroy-curiosity_core_c-qjhiuhbna-'):
                await self.sendCodeBlock(ctx, "http", Stage25.text1)
                await self.sendCodeBlock(ctx, "diff", Stage25.text2)
                await self.sendCodeBlock(ctx, "http", Stage25.text3)
                break;
            if case('aperture-science-glados-intelligence_core-pqlaidjeu-'):
                await self.sendCodeBlock(ctx, "diff", Stage26.text1)
                await self.sendCodeBlock(ctx, "diff", Stage26.text2)
                break;
            if case('aperture-science-destroy_intelligence_core_c-ufyhgiuy-'):
                await self.sendCodeBlock(ctx, "http", Stage27.text1)
                await self.sendCodeBlock(ctx, "diff", Stage27.text2)
                await self.sendCodeBlock(ctx, "http", Stage27.text3)
                break;
            if case('aperture-science-glados-anger_core-kwispelsj-'):
                await self.sendCodeBlock(ctx, "diff", Stage28.text1)
                await self.sendCodeBlock(ctx, "diff", Stage28.text2)
                break;
            if case('aperture-science-destroy_anger_core_c-nowescape-'):
                await self.sendCodeBlock(ctx, "http", Stage29.text1)
                await self.sendCodeBlock(ctx, "diff", Stage29.text2)
                await self.sendCodeBlock(ctx, "diff", Stage29.text3)
                break;
            if case('aperture-science-hoopy-the-hoop-glados_gib_10-'):
                await self.sendCodeBlock(ctx, "diff", Stage30.text1)
                break;
    
    async def userProgress(self, onstage, user):
        member_settings = self.config.member(user)
        curr_stage = await member_settings.stage()
        if curr_stage > onstage:
            pass
        else:
            await member_settings.stage.set(onstage)           
            if onstage > 1:
                await member_settings.stagefinished[onstage - 1].set("2020-01-01 04:40:45")
    
    async def sendCodeBlock(self, ctx, language: str, msg: str):
        msg = msg.replace("{author.id}", str(ctx.author.id)) 
        msg = msg.replace("{author.name}", str(ctx.author.name))
        embed = discord.Embed(color=0xEE2222, title='Test')
        embed.add_field(name='Computer output', value=box(msg, lang=language))
        embed.set_footer(text="This message will selfdestruct in: {} seconds".format(self.selfdestructtimer))
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
        return await self.config.guild(guild).wlchannels()
        
    async def _add_guild_channel(self, guild, channel):
        async with self.config.guild(guild).wlchannels() as chanlist:
            chanlist.append(channel)
            
    async def _toggle_whitelist(self, guild):
        wl = await self.config.guild(guild).whitelist()
        if wl:
            await self.config.guild(guild).whitelist.set(False)
            return False
        else:
            await self.config.guild(guild).whitelist.set(True)
            return True
            
    async def _remove_guild_channel(self, guild, channel):
        async with self.config.guild(guild).wlchannels() as chanlist:
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
            await ctx.send("Channel added")
        else:
            await ctx.send("Channel already whitelisted")
            
    @whitelist.command(name="toggle")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def toggle(self, ctx):
        """Toggle whitelist on/off."""
        new = await self._toggle_whitelist(ctx.guild)
        verb = "activated." if new else _("deactivated.")
        await ctx.send("Whitelist is {verb}".format(verb=verb))

    @whitelist.command(name="remove")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _remove(self, ctx, channel: discord.TextChannel = None):
        """Delete a channel from the whitelist."""
        if channel is None:
            channel = ctx.channel
        if channel.id not in await self._get_guild_channels(ctx.guild):
            await ctx.send("This channel isn't whitelisted.")
        else:
            await self._remove_guild_channel(ctx.guild, channel.id)
            await ctx.send("Channel deleted")

    @whitelist.command(name="show")
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def _show(self, ctx):
        """Show the list of channels configured to allow earning experience."""
        emb = discord.Embed()
        emb.title = "List of channels configured to allow enrichment commands."
        emb.description = "All things in the world aren't round there are red things too"
        channels = await self._get_guild_channels(ctx.guild)
        if not len(channels):
            return await ctx.send("No channels configured")
        emb.add_field(
            name="Channels:", value="\n".join([ctx.guild.get_channel(x).mention for x in channels])
        )
        await ctx.send(embed=emb)

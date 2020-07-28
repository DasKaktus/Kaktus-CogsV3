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
from .endcredits1 import Endcredits1
from .endcredits2 import Endcredits2
from .endcredits3 import Endcredits3
from .endcredits4 import Endcredits4
from .endcredits5 import Endcredits5
from .endcreditscakerecipe import EndcreditsCakeRecipe


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
    
    # Settings variables
    default_member = {"stage": 0, "started": "0000-00-00 00:00:00", "stagefinished": {"1": "0000-00-00 00:00:00", "2": "0000-00-00 00:00:00", "3": "0000-00-00 00:00:00", "4": "0000-00-00 00:00:00", "5": "0000-00-00 00:00:00", "6": "0000-00-00 00:00:00", "7": "0000-00-00 00:00:00", "8": "0000-00-00 00:00:00", "9": "0000-00-00 00:00:00", "10": "0000-00-00 00:00:00", "11": "0000-00-00 00:00:00", "12": "0000-00-00 00:00:00", "13": "0000-00-00 00:00:00", "14": "0000-00-00 00:00:00", "15": "0000-00-00 00:00:00", "16": "0000-00-00 00:00:00", "17": "0000-00-00 00:00:00", "18": "0000-00-00 00:00:00", "19": "0000-00-00 00:00:00", "20": "0000-00-00 00:00:00", "21": "0000-00-00 00:00:00", "22": "0000-00-00 00:00:00", "23": "0000-00-00 00:00:00", "24": "0000-00-00 00:00:00", "25": "0000-00-00 00:00:00", "26": "0000-00-00 00:00:00", "27": "0000-00-00 00:00:00", "28": "0000-00-00 00:00:00", "29": "0000-00-00 00:00:00", "30": "0000-00-00 00:00:00"}}
    default_guild = {"wlchannels": [], "whitelist": True }
    
    # Variables
    selfdestructtimer = 60
    selfdestructtimerreport = 30
    footertext = "This message will selfdestruct in: {}"
    
    # COG Stuff
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784274133784274, force_registration=True)
        self.config.register_member(**self.default_member)
        self.config.register_guild(**self.default_guild)
        self.messageids = []
        self.messageidslast = []
        self.msgtimer = {}
        self.msgtimerdelete = []
        self.msglasttimer = {}
        self.messageTimer.start()
        self.messageLastTimer.start()
    
    def cog_unload(self):
        self.messageTimer.cancel()
        self.messageLastTimer.cancel()
        
    # Mod commands
    
    @commands.command()
    @checks.mod_or_permissions(manage_messages=True)
    async def clearprogress(self, ctx, user: discord.Member):
        """Clears a users progress."""
        try:
            await ctx.message.delete()
        except Exception:
            pass
            
        if user is None:
            pass
        member_settings = self.config.member(user)
        await member_settings.stage.set(0)
        await member_settings.started.set("0000-00-00 00:00:00")
        for x in range(1, 31):
            await getattr(member_settings.stagefinished, str(x)).set("0000-00-00 00:00:00")
            
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
    
    # User commands
    
    @commands.command()
    async def whichstage(self, ctx):
        """Shows progress report."""
        user = ctx.author
        member_settings = self.config.member(user)
        curr_stage = await member_settings.stage()
        
        try:
            await ctx.message.delete()
        except Exception:
            pass
        
        if curr_stage > 1:
            curr_lastfinish = await getattr(member_settings.stagefinished, str(curr_stage - 1))()
        else:
            curr_lastfinish = "0000-00-00 00:00:00"
        
        embed = discord.Embed(color=0xEE2222, title='Test Progress Report')
        if curr_stage == 0:
            embed.add_field(name='Stage', value="N/A")
        else:
            embed.add_field(name='Stage', value=curr_stage)
        if curr_lastfinish == "0000-00-00 00:00:00":
            embed.add_field(name='Last stage finished', value="N/A")
        else:
            embed.add_field(name='Last stage finished', value=curr_lastfinish)
        #embed.set_footer(text="This message will selfdestruct in {} seconds".format(self.selfdestructtimer))
        embed.set_footer(text="Aperture Science Personnel File; #{}\nTest Subject Name; {}\n\nThis message will selfdestruct in: {}".format(user.id,user.name,self.selfdestructtimerreport))
        sendit = await ctx.send(embed=embed)
        self.messageids.append(sendit.id)
        self.ctx = ctx
        
    # Puzzle commands
    
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
            print("Enrichmentcenter (Error: 1): No permission to delete message")
            pass
            
        for case in switch(cclower):
            if case('aperture-science-help'):
                await self.sendCodeBlockEmbed(ctx, "http", Helptext.text1)
                break
            if case('aperture-science-initiate'):
                await self.setUserProgress(1, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage1.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage1.text2)
                break
            if case('aperture-science-c-uhswhbcjh-'):
                await self.setUserProgress(2, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage2.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage2.text2)
                break
            if case('aperture-science-c-dgwrgdfg-'):
                await self.setUserProgress(3, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage3.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage3.text2)
                break
            if case('aperture-science-c-fsdfswefs-'):
                await self.setUserProgress(4, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage4.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage4.text2)
                break;
            if case('aperture-science-c-xdergwerg-'):
                await self.setUserProgress(5, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage5.text1)
                break;
            if case('aperture-science-c-gsresdfgd-'):
                await self.setUserProgress(6, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage6.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage6.text2)
                break;
            if case('aperture-science-c-pfiejchen-'):
                await self.setUserProgress(7, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage7.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage7.text2)
                break;
            if case('aperture-science-c-fayhsdbfg-'):
                await self.setUserProgress(8, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage8.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage8.text2)
                break;
            if case('aperture-science-c-hiauhdiua-'):
                await self.setUserProgress(9, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage9.text1)
                break;
            if case('aperture-science-c-safhsiuhf-'):
                await self.setUserProgress(10, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage10.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage10.text2)
                break;
            if case('aperture-science-c-oudfhaiuh-'):
                await self.setUserProgress(11, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage11.text1)
                await self.sendCodeBlockEmbed(ctx, "fix", Stage11.text2)
                break;
            if case('aperture-science-c-sujdbisud-'):
                await self.setUserProgress(12, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage12.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage12.text2)
                break;
            if case('aperture-science-c-asijsihug-'):
                await self.setUserProgress(13, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage13.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage13.text2)
                break;
            if case('aperture-science-c-udjfhbaiu-'):
                await self.setUserProgress(14, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage14.text1)
                break;
            if case('aperture-science-incinerate_faithful_companion_cube'):
                await self.setUserProgress(15, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage15.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage15.text2)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage15.text3)
                break;
            if case('aperture-science-c-oeisoijfh-'):
                await self.setUserProgress(16, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage16.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage16.text2)
                break;
            if case('aperture-science-cake-whoah-yeah-cccccccake-'):
                await self.setUserProgress(17, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage17.text1)
                break;
            if case('aperture-science-c-jhfbishjg-goodbye-'):
                await self.setUserProgress(18, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage18.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage18.text2)
                break;
            if case('aperture-science-escape_glados_c-oiufhiuhi-'):
                await self.setUserProgress(19, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage19.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage19.text2)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage19.text3)
                break;
            if case('aperture-science-escape_glados_c-dahdgbuyh-'):
                await self.setUserProgress(20, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage20.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage20.text2)
                break;
            if case('aperture-science-confront-glados-central-ai-chamber-'):
                await self.setUserProgress(21, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage21.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage21.text2)
                await self.sendCodeBlockEmbed(ctx, "http", Stage21.text3)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage21.text4)
                break;
            if case('aperture-science-glados-morality_core-jhfgbiuyd-'):
                await self.setUserProgress(22, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage22.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage22.text2)
                break;
            if case('aperture-science-destroy_morality_core_c-caijhiujd-'):
                await self.setUserProgress(23, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage23.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage23.text2)
                await self.sendCodeBlockEmbed(ctx, "http", Stage23.text3)
                break;
            if case('aperture-science-glados-curiosity-core-wockdjehc-'):
                await self.setUserProgress(24, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage24.text1)
                await self.sendCodeBlockEmbed(ctx, "fix", Stage24.text2)
                break;
            if case('aperture-science-destroy-curiosity_core_c-qjhiuhbna-'):
                await self.setUserProgress(25, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage25.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage25.text2)
                await self.sendCodeBlockEmbed(ctx, "http", Stage25.text3)
                break;
            if case('aperture-science-glados-intelligence_core-pqlaidjeu-'):
                await self.setUserProgress(26, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage26.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage26.text2)
                break;
            if case('aperture-science-destroy_intelligence_core_c-ufyhgiuy-'):
                await self.setUserProgress(27, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage27.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage27.text2)
                await self.sendCodeBlockEmbed(ctx, "http", Stage27.text3)
                break;
            if case('aperture-science-glados-anger_core-kwispelsj-'):
                await self.setUserProgress(28, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage28.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage28.text2)
                break;
            if case('aperture-science-destroy_anger_core_c-nowescape-'):
                await self.setUserProgress(29, message.author)
                await self.sendCodeBlockEmbed(ctx, "http", Stage29.text1)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage29.text2)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage29.text3)
                break;
            if case('aperture-science-hoopy-the-hoop-glados_gib_10-'):
                await self.setUserProgress(30, message.author)
                await self.sendCodeBlockEmbed(ctx, "diff", Stage30.text1)
                break;
            if case('aperture-science-endcredits-glados-sa-1'):
                await self.sendCodeBlock(ctx, "http", Endcredits1.text1, False)
                break;
            if case('aperture-science-endcredits-glados-sa-2'):
                await self.sendCodeBlock(ctx, "http", Endcredits2.text1, False)
                break;
            if case('aperture-science-endcredits-glados-sa-3'):
                await self.sendCodeBlock(ctx, "http", Endcredits3.text1, False)
                break;
            if case('aperture-science-endcredits-glados-sa-4'):
                await self.sendCodeBlock(ctx, "http", Endcredits4.text1, False)
                await self.sendCodeBlock(ctx, "diff", Endcredits4.text2, False)
                break;
            if case('aperture-science-endcredits-thanks-for-playing'):
                await self.sendCodeBlock(ctx, "fix", Endcredits5.text1, False)
                await self.sendCodeBlock(ctx, "diff", Endcredits5.text2, False)
                break;
            if case('aperture-science-cake-core-recipe-'):
                await self.sendCodeBlock(ctx, "diff", EndcreditsCakeRecipe.text1, False)
                break;
    
    # Functions
    
    async def setTimer(self, msgid: int):
        self.msgtimer[sendit.id] = self.selfdestructtimer
        
    async def setUserProgress(self, onstage, user):
        member_settings = self.config.member(user)
        curr_stage = await member_settings.stage()
        if curr_stage > onstage:
            pass
        else:
            await member_settings.stage.set(onstage)           
            if onstage > 1:
                now = datetime.now()
                dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
                await getattr(member_settings.stagefinished, str(onstage - 1)).set(dt_string)
                
    async def fixPlaceholderText(self, ctx, msg):
        msg = msg.replace("{author.id}", str(ctx.author.id)) 
        msg = msg.replace("{author.name}", str(ctx.author.name))
        return msg
        
    async def sendCodeBlock(self, ctx, language: str, msg: str, embed = True):
        msg = fixPlaceholderText(ctx, msg)
        if embed:
            embed = discord.Embed(color=0xEE2222, title='Aperture Science Laboratories')
            embed.add_field(name='Computer-Aided Enrichment Center', value=box(msg, lang=language))
            embed.set_footer(text="This message will selfdestruct in: {}".format(self.selfdestructtimer))
            sendit = await ctx.send(embed=embed)
        else:
            sendit = await ctx.send(box(msg, lang=language))
        self.msgtimer[sendit.id] = self.selfdestructtimer    
        #self.messageids.append(sendit.id)
        self.ctx = ctx
        
    async def editMessageTimer(self, message, timeleft):
        # Check if embed    
        try:
            if message.embeds[0].fields[0].name == "Stage":
                #Progress card
                newembed = discord.Embed(color=0xEE2222, title=message.embeds[0].title)
                newembed.add_field(name=message.embeds[0].fields[0].name, value=message.embeds[0].fields[0].value)
                newembed.add_field(name=message.embeds[0].fields[1].name, value=message.embeds[0].fields[1].value)
                newembed.set_footer(text=footertext.format(str(timeleft)))
            else:
                #Output
                newembed = discord.Embed(color=0xEE2222, title='Aperture Science Laboratories')
                newembed.add_field(name='Computer-Aided Enrichment Center', value=org_msg)
                newembed.set_footer(text=footertext.format(str(timeleft)))
            await message.edit(embed=newembed)
        except:
            # Not embed
            # Do nothing for now.
            pass

    # Task Loops
    @tasks.loop(seconds=10.0)
    async def messageTimer(self):
        if hasattr(self, 'ctx'):
            for msgid, timeleft in self.msgtimer.items():
                # Try to get message
                try:
                    message = await self.ctx.channel.fetch_message(msgid)
                except:
                    # Message is deleted
                    del self.msgtimer[msgid]
                    continue
                
                editMessageTimer(message, timeleft - 10)
                    
                # Reduce the time or move to the last timer
                if timeleft - 10 == 10:
                    del self.msgtimer[msgid]
                    self.msglasttimer[msgid] = 10
                else:
                    self.msgtimer[msgid] = timeleft - 10
                    
                    
    @tasks.loop(seconds=1.0)
    async def messageLastTimer(self):
        if hasattr(self, 'ctx'):
            for msgid, timeleft in self.msglasttimer.items():
                # Try to get message
                try:
                    message = await self.ctx.channel.fetch_message(msgid)
                except:
                    # Message is deleted
                    del self.msglasttimer[msgid]
                    continue
                editMessageTimer(message, timeleft - 1)    
                
                # Reduce the time or delete message
                if timeleft - 1 == 0:
                    del self.msglasttimer[msgid]
                    try:
                        await message.delete()
                    except:
                        pass
                else:
                    self.msgtimer[msgid] = timeleft - 1
                
    @messageTimer.before_loop
    async def before_messageTimer(self):            
        await self.bot.wait_until_ready()
        
    @messageLastTimer.before_loop
    async def before_messageLastTimer(self):            
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
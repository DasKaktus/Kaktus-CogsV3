import discord
import json
import aiohttp
from redbot.core import commands, checks, Config
from redbot.core.data_manager import bundled_data_path

class Stattracker(commands.Cog):

    __author__ = "OGKaktus (OGKaktus#5299)"
    __version__ = "2.0"
    
    # Settings variables
    default_guild = {"whitelist": [], "whitelist": True }

    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()     
    
        self.config = Config.get_conf(self, identifier=13378427411233784274, force_registration=True)
        
        self.config.register_guild(**self.default_guild)


    @commands.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def statsset(self, ctx):
        """Configuration commands."""
        pass
    
    @statsset.group()
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
        verb = "activated." if new else "deactivated."
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
	
    @commands.command(pass_context=True, no_pm=True, name="bfvstats")
    async def bfvstats(self, ctx, platform, *, playername):
        """Retrieves stats for BFV"""

        guild = ctx.message.guild
        channel = ctx.message.channel
		
        if await self.config.guild(guild).whitelist():
            if channel.id not in await self._get_guild_channels(ctx.message.author.guild):
                return
			
        #await self.bot.send_typing(channel)
        async with ctx.typing():
            try:
                p = {
                    'PSN': 2,
                    'PS4': 2,
                    'PLAYSTATION': 2,
                    'XBOX': 1,
                    'XB': 1,
                    'XB1': 1,
                    'X1': 1,
                    'PC': 3,
                    'MAC': 4,
                }
                pform = p.get(platform.upper(), 0)
                if pform:
                    if pform == 4:
                        await self.bot.say(ctx.message.author.mention + ", Ha ha ha ha ha... Mac.. You Sir are hilarious")
                    else:
                        url = 'https://www.baver.se/bfv/index.php?pf=' + str(pform) + '&user=' + playername.replace(" ", "%20")
                        await fetch_image(self, ctx, ctx.message.author, url, playername, platform)
                else:
                    await self.bot.say(ctx.message.author.mention + ", please specify a valid platform. (PSN, XBOX or PC)")
            except Exception as e:
                #await self.bot.say("error: " + e.message + " -- " + e.args)
                err = e.message

    def __unload(self):
        #
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


async def fetch_image(self, ctx, duser, urlen, user, platform):
    async with aiohttp.get(urlen) as response:
        if response.headers['Content-Type'] == "image/png":
            return await self.bot.send_file(ctx.message.channel, io.BytesIO(await response.read()), filename=user + '.png')
        else:
            return await self.bot.say("Sorry " + duser.mention + ", could not find the player `"+ user + "`")

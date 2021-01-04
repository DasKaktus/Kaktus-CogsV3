import aiohttp
import discord
from redbot.core import commands, checks, Config

class Inspiration(commands.Cog):
    """Inspiration Cog"""
    
    default_guild = {"wlchannels": [], "whitelist": True }
    
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=133784278133784274, force_registration=True)
        self.config.register_guild(**self.default_guild)
        self.session = aiohttp.ClientSession()
        
    @commands.command()
    async def getinspiration(self, ctx):
        """Get a random inspiration card."""
        
        message = ctx.message
        
        if await self.config.guild(message.guild).whitelist():
            if message.channel.id not in await self._get_guild_channels(message.author.guild):
                return
                
        try:
            async with self.session.request("GET", "http://inspirobot.me/api?generate=true") as page:
                card = await page.text(encoding="utf-8")
                em = discord.Embed()
                em.set_image(url=card)
                await ctx.send(embed=em)
        except Exception as e:
            await ctx.send(f"Oopsie: {e}")
        
    @commands.group()
    @checks.mod_or_permissions(manage_messages=True)
    @commands.guild_only()
    async def inspiration(self, ctx):
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
        emb.title = "List of channels configured to allow inspiration command."
        emb.description = "All things in the world aren't round there are red things too"
        channels = await self._get_guild_channels(ctx.guild)
        if not len(channels):
            return await ctx.send("No channels configured")
        emb.add_field(
            name="Channels:", value="\n".join([ctx.guild.get_channel(x).mention for x in channels])
        )
        await ctx.send(embed=emb)
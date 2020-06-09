from copy import copy
from redbot.core import commands
from redbot.core.utils.tunnel import Tunnel

class Morsedecoder(commands.Cog):
    """Morse Decoder cog"""

    @commands.command()
    async def decode(self, ctx):
        """Tries to decode morse from attached audio or video"""
        msg = copy(ctx.message)
        files: List[discord.File] = await Tunnel.files_from_attach(msg)
        for f in files:
            await ctx.send(f.filename)
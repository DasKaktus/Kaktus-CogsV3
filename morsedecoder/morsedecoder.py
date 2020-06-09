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
            await ctx.send(f.url)
        #max_size = 8 * 1000 * 1000
        #if msg.attachments and sum(a.size for a in m.attachments) <= max_size:
        #    for a in m.attachments:
        #        _fp = io.BytesIO()
        #        await a.save(_fp)
        #        files.append(discord.File(_fp, filename=a.filename))
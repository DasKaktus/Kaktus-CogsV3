import asyncio

import discord
from redbot.core import commands
import io
from typing import List, Optional

class Kaktusutils:
    @staticmethod
    async def files_from_attach(m: discord.Message) -> List[discord.File]:
        """
        makes a list of file objects from a message
        returns an empty list if none, or if the sum of file sizes
        is too large for the bot to send
        Parameters
        ---------
        m: `discord.Message`
            A message to get attachments from
        Returns
        -------
        list of `discord.File`
            A list of `discord.File` objects
        """
        files = []
        max_size = 8 * 1000 * 1000
        if m.attachments and sum(a.size for a in m.attachments) <= max_size:
            for a in m.attachments:
                _fp = io.BytesIO()
                await a.save(_fp)
                files.append(discord.File(_fp, filename=a.filename, url=a.url))
        return files
from .stattracker import Stattracker
import pathlib

path = 'data/kaktuscog/stattracker

def setup(bot):
    pathlib.Path(path).mkdir(exist_ok=True, parents=True)
    cog = Stattracker(bot)
    bot.add_cog(cog)

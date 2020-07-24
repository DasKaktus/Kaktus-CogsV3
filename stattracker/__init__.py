from .stattracker import Stattracker

def setup(bot):
    bot.add_cog(Stattracker(bot))
from .inspiration import Inspiration


def setup(bot):
    bot.add_cog(Inspiration(bot))

from .custcomimproved import CustomCommandsImproved


def setup(bot):
    bot.add_cog(CustomCommandsImproved(bot))

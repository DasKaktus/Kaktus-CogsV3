from .enrichmentcenter import EnrichmentCenter


def setup(bot):
    cog = EnrichmentCenter(bot)
    bot.add_cog(cog)
    await cog.initialise()

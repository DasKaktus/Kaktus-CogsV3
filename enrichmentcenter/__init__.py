from .enrichmentcenter import EnrichmentCenter


def setup(bot):
    bot.add_cog(EnrichmentCenter(bot))

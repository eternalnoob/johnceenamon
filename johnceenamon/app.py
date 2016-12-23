import discord
import logging
import flask

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

client = discord.Client()


@client.async_event
def on_ready():
    logger.info('Logged in as %s, id: %s', client.user.name, client.user.id)


def main():
    django.setup()  # configures logging etc.
    logger.info('Starting up bot')

    pool = MethodPool()  # pool that holds all callbacks
    event_pool = EventPool()
    for plugin, options in settings.PLUGINS.items():
        if not options.get('enabled', True):
            continue

        module = 'bot.plugins.%s' % plugin
        if module in settings.INSTALLED_APPS:
            module = '%s.plugin' % module
        _plugin = import_module(module)
        plugin = _plugin.Plugin(client, options)
        pool.register(plugin)
        event_pool.register(plugin)
        logger.debug('Configured plugin %r', plugin)

    # bind the callback pool
    pool.bind_to(client)

    # login & start
    client.run(settings.TOKEN)

def create_app():


if __name__ == '__main__':
    main()




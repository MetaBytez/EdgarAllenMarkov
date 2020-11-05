from logging import getLogger, basicConfig, INFO
from time import sleep

from tweepy_parrot import ParrotBot

from syllable_parrot import HaikuException, SyllableParrot

basicConfig(
    filename='bot.log',
    filemode='w+',
    level=INFO, 
)

logger = getLogger(__name__)

parrot = SyllableParrot('parrot.json')
bot = ParrotBot(parrot)
bot.start(True, True)

while True:
    try:
        logger.info(f'\nPolly Says:\n\n{bot.squawk()}\n')
    except IndexError:
        logger.error('Nothing to Squawk at')
    except HaikuException:
        logger.error('Not enough data to get creative')

    sleep(5*60)

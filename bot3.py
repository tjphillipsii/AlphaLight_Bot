import discord
from discord.ext import commands
import json
import logging
from random import choice
from datetime import datetime
import aiohttp
import secrets

logger = logging.getLogger('discord')
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('shaxx.txt', 'r') as f:
    shaxx = f.read().splitlines()

description = "Alpha Light's little shitposter"

bot = commands.Bot(command_prefix='!', description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------------')


@bot.command()
async def test():
    """Check to see if the bot is running"""
    await bot.say("Testing? Testing.... Yep I am alive!")


@bot.command()
async def getsum():
    """Returns a random quote from Shaxx"""
    await bot.say(choice(shaxx))


@bot.command(pass_context=True)
async def hug(ctx, *, member: discord.Member = None):
    """Something silly"""
    if member is None:
        await bot.say(ctx.message.author.mention + " has been hugged!")
    else:
        await bot.say(member.mention + " has been hugged by " + ctx.message.author.mention)


@bot.command(pass_context=True, description="Takes a string, deletes your messages, and says what you said.")
async def echo(ctx, *, echo: str = None):
    """Really bad attempt at a joke.. or something."""
    if echo is None:
        await bot.say("You need to enter some text for me to say...")
    else:
        await bot.delete_message(ctx.message)
        await bot.say(":slight_smile: " + echo)


@bot.command(pass_context=True)
async def chstat(ctx, *, activity: str = None):
    """Currently only Agent can run this command."""
    if ctx.message.author.id == "97077596092633088":
        if activity is None:
            await bot.say("Looks like you forgot to include a status...")
        else:
            await bot.change_presence(game=discord.Game(name=activity))
    else:
        await bot.say("I am sorry Dave... I can't let you do that")


@bot.command(pass_context=True)
async def kenny(ctx):
    """T I double Grrr POTATO!"""
    await bot.say('Ummm.... POTATO!')
    await bot.send_file(ctx.message.channel, 'kennythetiger.jpg')


@bot.command()
async def joined(member: discord.Member = None):
    """Tells you when a member joined."""
    if member is None:
        await bot.say('Sorry, but you need to enter a user to check.')
    else:
        await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.command()
async def nightfall():
    """Here is the Nightfall for the week, with burns."""
    url = 'https://www.bungie.net/d1/Platform/Destiny/Advisors/?definitions=True'
    async with aiohttp.get(url, headers=secrets.HEADERS) as r:
        if r.status == 200:
            rootdata = await r.json()
            data = rootdata['Response']
            bundle = str(data['data']['nightfall']['activityBundleHash'])
            nighthash = str(data['data']
                            ['nightfall']
                            ['tiers']
                            [0]
                            ['activityHash']
                            )
            nightfall = (data['definitions']
                         ['activities']
                         [nighthash]
                         ['activityName'])
            skullindex = data['data']['nightfall']['tiers'][0]['skullIndexes']
            burns = []
            skullindex = list(skullindex)
            for item in skullindex:
                burns.append(data['definitions']
                             ['activities'][bundle]
                             ['skulls'][item]['displayName'])
            await bot.say('The Nightfall for the week is:\n{}\nThe burns are:\n{}'.format(nightfall, '\n'.join(burns)))

bot.run(secrets.TOKEN, bot=True, reconnect=True)

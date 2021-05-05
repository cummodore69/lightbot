import re
import random
import logging

from discord.ext import commands, tasks
import discord
import process_yaml

logging.basicConfig(level=logging.INFO)

process_yaml = process_yaml.ProcessYaml()
config = process_yaml.config
config_commands = config['commands']
config_info = config['bot-info']

prefix = config_info['prefix']
status = config_info['status']
token = config_info['token']

print(status[1])

# Define the bot variable and define the prefix
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online)
    print('We have logged in as {0.user}'.format(bot))
    print('bot is now working lol')
    if config['rainbow-role']:
        change_color.start()

    if config['out-of-pepsi']:
        out_of_pepsi.start()

    if config['random-status']:
        random_status.start()

    if config['out-of-pills']:
        out_of_pills.start()


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if config['beta-mode'] and message.channel.id != 796101319542702120:
        return

    fol_pattern = r"(?:^|\W)fol(?:$|\W)"  # Everytime someone says "fol" send the emote ":cringe:"
    if re.search(fol_pattern, message.content.lower()) is not None:
        channel = message.channel
        await channel.send("<:cringe:796041237038759977>")

    pepsi_pattern = r"(?:^|\W)pepsi(?:$|\W)"  # Everytime someone says "pepsi" say "*drinks another can of pepsi*"
    if re.search(pepsi_pattern, message.content.lower()) is not None:
        channel = message.channel
        await channel.send("*drinks another 1L bottle of pepsi*")

    # This is needed for commands to run. Please refer to
    # last post on this thread:
    # https://forum.omz-software.com/topic/5684/discord-py-1-2-2-bot-doesn-t-respond-to-commands/
    await bot.process_commands(message)


if config_commands['ping']:
    @bot.command(name='ping')
    async def ping(ctx):
        await ctx.send(f"bonk! {round(bot.latency * 1000)}ms")

if config_commands['test']:
    @bot.command(name='test')
    async def test(ctx):
        await ctx.send('yes i work UwU')

if config_commands['pepsi']:
    @bot.command(name='pepsi')
    async def pepsi(ctx):
        await ctx.channel.send('yes please')


@tasks.loop(minutes=5)
async def change_color():
    rainbow = None
    for guild in bot.guilds:
        for role in guild.roles:
            if role.id == 796461375412633641:
                rainbow = role
        await rainbow.edit(color=discord.Color.from_hsv(random.random(), 1, 1))


@tasks.loop(hours=3)
async def out_of_pepsi():
    for guild in bot.guilds:
        channel = guild.get_channel(795801218626486294)
        await channel.send("Guys I'm out of pepsi :(")


@tasks.loop(hours=5)
async def out_of_pills():
    for guild in bot.guilds:
        channel = guild.get_channel(795801218626486294)
        await channel.send("Guys I'm out of caffeine pills :(")


@tasks.loop(minutes=2)
async def random_status():
    new_status = random.choice(status)
    print(f"Changing status to: {new_status}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(new_status))


bot.run(token)

# Comments by E404NNF.

# Import Regex, Random and Logging
import re
import random
import logging

# Import commands and tasks from discord.ext, import discord.py and the YAML processor (in the same directory).
from discord.ext import commands, tasks
import discord
import process_yaml

# Set logging level to basic info
logging.basicConfig(level=logging.INFO)

# Load config variables
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

    # Start the tasks if their config options are set to true
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

    # If beta-mode in the config is enabled and the message channel id isn't 796101319542702120 then don't send anything
    if config['beta-mode'] and message.channel.id != 796101319542702120:
        return

    # Everytime someone says "fol" send the emote ":cringe:"
    fol_pattern = r"(?:^|\W)fol(?:$|\W)" # Regex to check for the word "fol" in any case (use https://regexr.com/ to check out how it works)
    # Use re to check if the pattern 
    # we just defined is in the message (after lowercasing it)
    if re.search(fol_pattern, message.content.lower()) is not None: 
        channel = message.channel
        await channel.send("<:cringe:796041237038759977>")

    # Everytime someone says pepsi send "*drinks another 1L bottle of pepsi*"
    pepsi_pattern = r"(?:^|\W)pepsi(?:$|\W)" # Regex to check for the word "pepsi" in any case (use https://regexr.com/ to check out how it works)
    # Use re to check if the pattern
    # we just defined is in the message (after lowercasing it)
    if re.search(pepsi_pattern, message.content.lower()) is not None:
        channel = message.channel
        await channel.send("*drinks another 1L bottle of pepsi*")

    # This is needed for commands to run. Please refer to
    # last post on this thread:
    # https://forum.omz-software.com/topic/5684/discord-py-1-2-2-bot-doesn-t-respond-to-commands/
    await bot.process_commands(message)

# If the config option of the any of these commands is set to true then check for the command
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


# Rainbow role task, changes role color every 5 minutes.
@tasks.loop(minutes=5)
async def change_color():
    rainbow = None
    for guild in bot.guilds:
        for role in guild.roles:
            if role.id == 796461375412633641:
                rainbow = role
        await rainbow.edit(color=discord.Color.from_hsv(random.random(), 1, 1))



# Loops below are for the messages tasks.
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


# Random status
@tasks.loop(minutes=2)
async def random_status():
    new_status = random.choice(status) # Choose a random status from the config option we defined
    print(f"Changing status to: {new_status}")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(new_status))


bot.run(token)

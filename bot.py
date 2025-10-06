import discord
import os
import asyncio
import time
import random

names = ...
insults = ... 
with open('names-insults.txt') as f:
    lines = f.read().split('\n')
    names = lines[0].split(',')
    insults = lines[1].split(',')

token = ...
with open('token') as f:
    token = f.read()

images_path = '/home/onaquest/server-output/images'

# init bot 
#intents = 109632
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.reactions = True

client = discord.Client(intents=intents)

def make_insult():
    name = names[random.randint(0, len(names) - 1)]
    insult = insults[random.randint(0, len(insults) - 1)]

    if random.randint(0, 2) == 0: 
        name = name.upper()
    if random.randint(0, 2) == 0: 
        insult = insult.upper()

    return f'{name} is a {insult}'


# returns discord file object 
def get_recent_image(images_path):
    recent_path = max(os.listdir(images_path))
    return discord.File(f'{images_path}/{recent_path}')

@client.event
async def on_ready(): 
    guild = client.get_guild(516440617199337506) # henry's cage ID
    channel = guild.get_channel(1406777331053232208) # mushroom chat ID 
    asyncio.create_task(autosend(channel))

@client.event 
async def on_message(message):
    if message.content == 'please give me an image':
        sent_msg = await message.reply(make_insult(), file=get_recent_image(images_path))   
        #add reaction

async def autosend(channel):
    await client.wait_until_ready()
    time.sleep(0.5)
    while not client.is_closed():
        sent_msg = await channel.send(make_insult(), file=get_recent_image(images_path)) 
        await asyncio.sleep(4*60*60)

client.run(token)


import discord
import os
import asyncio
import time
import random

names = ...
insults = ...
get_insult_supplies()

emojis = ...
with open('emojis.txt') as f:
    emojis = f.read().split(',')

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

def get_insult_supplies():   
    global names
    global insults 
    with open('names.txt') as f:
        names = f.read().split('\n')
    with open('insults.txt') as f:
        insults = f.read().split('\n')

def random_emoji():
    return emojis[random.randint(0, len(emojis) - 1)]

def make_insult():
    get_insult_supplies()
    name = names[random.randint(0, len(names) - 1)]
    insult = insults[random.randint(0, len(insults) - 1)]

    if random.randint(0, 2) == 0: 
        name = name.upper()
    if random.randint(0, 2) == 0: 
        insult = insult.upper()

    return f'{name} is a {insult}'


# returns discord file object 
def get_recent_image(images_path, id):
    recent_path = max(os.listdir(f'{images_path}{id}'))
    return discord.File(f'{images_path}{id}/{recent_path}')

@client.event
async def on_ready(): 
    guild = client.get_guild(516440617199337506) # henry's cage ID
    channel = guild.get_channel(1406777331053232208) # mushroom chat ID 
    asyncio.create_task(autosend(channel))

@client.event 
async def on_message(message):
    if message.content == 'please give me an image':
        sent_msg = await message.reply('ugh. looks like *somebody* didnt get the memo 🙄\nyou have to say \"top\" \"side"\" or \"both\" at the end now dumbass')   
        await sent_msg.add_reaction(random_emoji())
    if message.content == 'please give me an image top':
        sent_msg = await message.reply(make_insult(), file=get_recent_image(images_path, 0))   
        await sent_msg.add_reaction(random_emoji())
    if message.content == 'please give me an image side':
        sent_msg = await message.reply(make_insult(), file=get_recent_image(images_path, 1))   
        await sent_msg.add_reaction(random_emoji())
    if message.content == 'please give me an image both':
        sent_msg = await message.reply(make_insult(), files=[get_recent_image(images_path, 0), get_recent_image(images_path, 1)])   
        await sent_msg.add_reaction(random_emoji())
    
    if message.content.startswith('please mr shroombot can i add this insult:') and len(message.content) > 42:
        added_insult = message.content.split(':')[1].trim()
        with open('insults.txt', 'a') as f:
            f.write(f'{added_insult}\n')
        sent_msg = await message.reply(f'ok i did it. i added {added_insult}')
        sent_msg.add_reaction('🙂‍↕️')

async def autosend(channel):
    await client.wait_until_ready()
    time.sleep(0.5)
    while not client.is_closed():
        sent_msg = await channel.send(make_insult(), files=[get_recent_image(images_path, 0), get_recent_image(images_path, 1)]) 
        await sent_msg.add_reaction(random_emoji())
        await asyncio.sleep(4*60*60)

client.run(token)


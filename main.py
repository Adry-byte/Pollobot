import os # Library of the operating system
import discord # Library of the API discord.py
from discord.ext import commands
from music_cog import music_cog
from keep_awake import keep_alive
#Rodri code below
#from discord.ext import commands
#import music


#cogs = [music]

#client = commands.Bot(command_prefix='?', intents = discord.Intents.all())
#client.run('ODg4MTI2MDA2NDI5MzcyNDU2.YUOJzA.Z-vHEnjib-OVR6l3KVCMTSwprjo')


#for i in range(len(cogs)):
#    cogs[i].setup(client)

# Fin Rodri code

my_secret = os.environ['TOKEN'] # TOKEN of PolloBot
bot = commands.Bot('!', description='PolloBot.')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.event
async def on_message(message):
    aux = message.content.lower() # To make the message all in lowercase
    if message.author == bot.user:
        return

    if aux == 'oscar' or aux == 'juan carlos':
        await message.channel.send('Chupapijas')

    elif aux == 'elias':
        await message.channel.send('Mi economia se basa en talar arboles')
    
    elif aux == 'adryh' or aux == 'adri' or aux == 'rodri':
        await message.channel.send('Dios supremo del Papá Pollo')
    
    elif aux == 'fer' or aux == 'keor98' or aux == 'keor94' or aux == 'keor':
        await message.channel.send('Siempre me encuentro a la gente de espalda GG WP EZ')

    elif aux == 'pollo':
        await message.channel.send('🐔')



bot.add_cog(music_cog(bot))

keep_alive()

bot.run(my_secret)
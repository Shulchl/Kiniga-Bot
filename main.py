import discord, os, asyncio, random, re
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix = ".", intents=intents)
client.remove_command('help')

f = ''

@client.event
async def on_ready():
    try:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="kiniga.com"))
        print(f'Tudo perfeito!')
    except:
        print(f'Não foi possivel adicionar uma atividade.')

@client.event
async def feed():
    await client.wait_until_ready()
    while not client.is_closed():
        soup = BeautifulSoup(requests.get("http://kiniga.com/").text,'lxml')
        table = soup.find('table', attrs={'class':'manga-chapters-listing'})
        titles = table.find_all('td', attrs={'class':'title'})[0]
        for t in titles:
            try:
                links = table.find_all('td', attrs={'class':'release'})[0]
                for l in links.find_all('a', href=True):
                    try:
                        with open('r.txt', 'w+') as prevUpdate:
                            if l['href'] != prevUpdate.read():
                                global f
                                if f == l['href']:
                                    prevUpdate.close()
                                    return await asyncio.sleep(300)
                                else:
                                    channel = discord.utils.get(client.get_all_channels(), guild__name='Kiniga Brasil', name='✶⊷彡recentes')
                                    await channel.send('Saiu o **{}** de **{}**!\n\n{}'.format(l.get_text(), t.get_text(), l['href']))
                                    f = l['href']
                                    prevUpdate.write(f)
                                    prevUpdate.close()
                                    return await asyncio.sleep(300)
                    except: 
                        return await asyncio.sleep(30)
            except:
                return await asyncio.sleep(30)
            
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Olha, eu chuto que esse comando não existe...')
        await asyncio.sleep(1)
        await ctx.channel.purge(limit=2)

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"I have loaded the command")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send("I have reloaded the command")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send("I have unloaded the command")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.create_task(feed())

client.run("TOKEN")

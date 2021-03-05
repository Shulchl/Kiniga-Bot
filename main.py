import discord, os, asyncio, random, re
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

client = commands.Bot(command_prefix = ".")
client.remove_command('help')

f = ''

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
                        global f
                        if f == l['href']:
                            await asyncio.sleep(30)
                        else:
                            channel = discord.utils.get(client.get_all_channels(), guild__name='Servidor de Shuichiff', name='geral')
                            await channel.send('Saiu o **{}** de **{}**!'.format(l.get_text(), t.get_text()))
                            await channel.send('Leia aqui: {}'.format(l['href']))
                            f = l['href']
                            
                            await asyncio.sleep(30)
                    except: 
                        await asyncio.sleep(3)
            except:
                await asyncio.sleep(3)
            
            
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{error}')

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

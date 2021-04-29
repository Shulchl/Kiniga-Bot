import discord, os, asyncio, re
from discord.ext import commands
import requests
from bs4 import BeautifulSoup

intents = discord.Intents().all()
intents.members = True

client = commands.Bot(command_prefix = ".", 
                      intents=intents, 
                      activity = discord.Activity(type=discord.ActivityType.watching, name="[Kiniga.com] — Leia e escreva histórias!"), 
                      status=discord.Status.online)

client.remove_command('help')

f = ''

@client.event
async def on_ready():
    try:
        print('Tudo perfeito!')
    except:
        return print('Algo deu errado. Reinicie e tente novamente.')

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
                        channel = discord.utils.get(client.get_all_channels(), 
                                                    guild__name='Kiniga Brasil', 
                                                    name='✶⊷彡recentes')
                        messages = await channel.history(limit=1).flatten()
                        messages.reverse()
                        cont = 'Saiu o **{}** de **{}**!\n{}'.format(l.get_text(),
                                                                    t.get_text(),
                                                                    l['href'])
                        for i, message in enumerate(messages):
                            message = message.content
                            if message == cont:
                                await asyncio.sleep(300)
                            else:
                                await channel.send(cont)
                                f = l['href']
                                await asyncio.sleep(300)
                    except: 
                        await asyncio.sleep(300)
            except:
                await asyncio.sleep(300)
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Olha, eu chuto que esse comando não existe...')

@client.command()
@commands.is_owner()
async def load(self, ctx, extension):
    self.load_extension(f'cogs.{extension}')
    await ctx.send("Carreguei os comandos")

@client.command()
@commands.is_owner()
async def reload(self, ctx, extension):
    self.unload_extension(f'cogs.{extension}')
    self.load_extension(f'cogs.{extension}')
    await ctx.send("Recarreguei os comandos")

@client.command()
@commands.is_owner()
async def unload(self, ctx, extension):
    self.unload_extension(f'cogs.{extension}')
    await ctx.send("Descarreguei os comandos")
                
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
                
client.loop.create_task(feed())

client.run(os.getenv('TOKEN'))

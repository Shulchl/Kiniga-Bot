from logging import raiseExceptions
import discord, os, asyncio
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
    
@client.event
async def feed():
    await client.wait_until_ready()
    while not client.is_closed():
        soup = BeautifulSoup(requests.get("http://kiniga.com/").text,'lxml')
        table = soup.find('table', attrs={'class':'manga-chapters-listing'})  
        titles = table.find('td', attrs={'class':'title'})
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
                        member = channel.guild.get_member(741770490598653993)
                        webhooks = await channel.webhooks()
                        webhook = discord.utils.get(webhooks, name = "Capitulos Recentes")
                        for i, message in enumerate(messages):
                            message = message.content
                            if message != cont:
                                if webhook is None:
                                    webhook = await channel.create_webhook(name = "Capitulos Recentes")
                                    
                                return await webhook.send(cont, username = member.name, avatar_url = member.avatar_url)
                                    
                            else: await asyncio.sleep(300)
                        else:
                            if webhook is None:
                                webhook = await channel.create_webhook(name = "Capitulos Recentes")
                                
                            return await webhook.send(cont, username = member.name, avatar_url = member.avatar_url)
                    except: raise
                else: return print("Não encontrei nenhum link")
            except: raise
        else: return print("Não encontrei nenhum titulo")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
                        
client.loop.create_task(feed())

client.run(os.getenv('TOKEN'))

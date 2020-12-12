import discord, os, asyncio, random, re
from discord.ext import commands
from datetime import date, datetime, timedelta  
import requests
from bs4 import BeautifulSoup

client = discord.Client()

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
                        f = open("r.txt", "r")
                        ler_l = f.read()
                        l_r = l['href']
                        if ler_l == l_r:
                            #print('Parece que não tem nada novo...')
                            await asyncio.sleep(300)
                        else:
                            channel = discord.utils.get(client.get_all_channels(), guild__name='Kiniga Brasil', name='✶⊷彡recentes')
                            await channel.send('Saiu o **{}** de **{}**!'.format(l.get_text(), t.get_text()))
                            await channel.send('Leia aqui: {}'.format(l['href']))
                            print('\n\nSaiu o {} de {}! \n\nLeia aqui: {} '.format(l.get_text(), t.get_text(), l['href']))
                            f = open("r.txt", "w")
                            f.write(l['href'])
                            f.close()
                            l_r = ''
                            await asyncio.sleep(30)
                    except: 
                        print('Não encontrei nenhum link...')
                        await asyncio.sleep(300)
                        pass
            except:
                print('Não encontrei nenhum titulo...')
                await asyncio.sleep(300)
                pass

client.loop.create_task(feed())

client.run(os.getenv('TOKEN'))

import discord, asyncio
from discord.ext import commands  
import requests
from bs4 import BeautifulSoup

class NoPrivateMessages(commands.CheckFailure):
    pass

def guild_only():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessages('Esse comando não pode ser usado em mensagens privadas!')
        return True
    return commands.check(predicate)

class Noticia(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Comando de notícias funcionando!    [√]')

    @guild_only()
    @commands.command(name='noticia', help='Anuncia no canal especificado ao digitar `.noticia [#canal] + [conteúdo]` ')
    @commands.has_permissions(administrator=True)
    async def noticia(self, ctx, channel: discord.TextChannel, message):
        ### Get text ###
        msg = []
        titulo = []
        msg = ctx.message.content.split()
        del msg[0]
        del msg[0]
        a = ' '.join(msg)
        a = str(a)
        a = a.strip('"')
        conteudo = a
        
        ### Get channel ###
        channel_name = ctx.message.content.split()
        del channel_name[0]
        a = ' '.join(channel_name)
        a = str(channel_name[0])
        a = a.strip('<')
        a = a.strip('>')
        a = a.strip('#')
        channel_id = a        
        channel_name = (channel for channel in self.client.get_all_channels() if channel.id == channel_id)
        
        ### Start the magic ###
        emb = discord.Embed(title='Certo!',description=f'Deseja usar "**{conteudo}**" como conteúdo da notícia?',color=discord.Color.orange()).set_footer(text='Para cancelar, basta aguardar.')
        msg = await ctx.send('',embed=emb)
        await msg.add_reaction('✔')
        await asyncio.sleep(1)
        def check(reaction, member):
            return member == ctx.author and str(reaction.emoji) == '✔'
        try:
            await self.client.wait_for('reaction_add',timeout=30.0, check=check)
            emb2 = discord.Embed(title='Digite o título!',description='*Cri, cri...*',color=discord.Color.orange()).set_footer(text='Para cancelar, basta aguardar.')
            await ctx.send('',embed=emb2)
            def check_2(message):
                return message.author.id == ctx.author.id and message.author.id != self.client.user.id
            try:
                titulo = await self.client.wait_for('message',timeout=30.0, check=check_2)
                titulo = titulo.content
                emb3 = discord.Embed(title='Certo!', description="Deseja usar\n\n**{}**\n\n... como título da notícia?".format(titulo), color=discord.Color.orange()).set_footer(text='Para cancelar, basta aguardar.')
                msg3 = await ctx.send('',embed=emb3)
                await msg3.add_reaction('✔')
                await asyncio.sleep(1)
                def check_3(reaction, member):
                    return reaction.message.id == msg3.id and str(reaction.emoji) == '✔'
                try:
                    await self.client.wait_for('reaction_add',timeout=10.0, check=check_3)
                    await asyncio.sleep(1)
                    await ctx.channel.purge(limit=4)
                    emb5 = discord.Embed(title='{}'.format(titulo),description='{}'.format(conteudo),color=discord.Color.green())
                    await channel.send('',embed=emb5)
                    return await ctx.send('A notícia foi enviada com sucesso')
                except asyncio.TimeoutError:
                    emb5 = discord.Embed(title='Hum...',description='Eu não recebi uma confirmação, que tal tentar de novo?.',color=discord.Color.orange())
                    await ctx.send('',embed=emb5)
                    await asyncio.sleep(3)
                    return await ctx.channel.purge(limit=2)
            except asyncio.TimeoutError:
                emb5 = discord.Embed(title='Hum...',description='Eu não recebi uma confirmação, que tal tentar de novo?.',color=discord.Color.orange())
                await ctx.send('',embed=emb5)
                await asyncio.sleep(3)
                return await ctx.channel.purge(limit=2)
        except asyncio.TimeoutError:
            emb5 = discord.Embed(title='Hum...',description='Eu não recebi uma confirmação, que tal tentar de novo?.',color=discord.Color.orange())
            await ctx.send('',embed=emb5)
            await asyncio.sleep(3)
            return await ctx.channel.purge(limit=2)
        else:
            emb5 = discord.Embed(title='Hum...',description='Você precisa marcar um canal válido. Esse eu não achei :c',color=discord.Color.red())
            await ctx.send('',embed=emb5)
            await asyncio.sleep(3)
            return ctx.channel.purge(limit=2)

    @guild_only()
    @commands.command(name='release', help='Anuncia o lançamento mais recente ao digitar `.release` ')
    @commands.has_permissions(administrator=True)
    async def release(self, ctx):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            soup = BeautifulSoup(requests.get("http://kiniga.com/").text,'lxml')
            table = soup.find_all('div', attrs={'class':'tab-content-wrap'})[3]
            novel_recente = table.find_all('div', attrs={'class':'page-item-detail'})[0]
            t = novel_recente.find_all('div', attrs={'class':'item-summary'})[0]
            title = t.find('div', attrs={'class':'post-title'})
            for t in title:
                try:
                    for l in title.find_all('a', href=True):
                        try:
                            novel = BeautifulSoup(requests.get(l['href']).text,'lxml')
                            link = l['href']                                            #link
                            titulo = title.get_text()                                   #titulo da história
                            author = novel.find('h4', attrs={'class':'nomedoautor'})    #nome do autor
                            
                            h = novel.find('div', attrs={'class':'divdobotao'})         #link do autor
                            author_link = h.find('a', href=True)
                            
                            s = novel.find('div', attrs={'class':'summary__content'})   #sinopse da história
                            sinopse = s.find('p').get_text()
                            
                            a = novel.find('div', attrs={'class':'backgroundautor'})    #img author
                            img_author = a.find_all('img', src=True)[0]
                            
                            i = novel.find('div', attrs={'class':'summary_image'}).find('img', {'class': 'img-responsive'})     #img novel
                            img = i.get('data-src')
                            channel = discord.utils.get(self.client.get_all_channels(), 
                                                        guild__name='Kiniga Brasil', 
                                                        id=678060799213830201)
                            emb = discord.Embed(title="📢 NOVA OBRA PUBLICADA 📢", url=link, color=discord.Color.green())
                            emb = emb.set_author(name=author.get_text(), url=author_link['href'], icon_url=img_author['src'])
                            emb = emb.set_thumbnail(url="https://kiniga.com/wp-content/uploads/fbrfg/favicon-32x32.png")
                            emb = emb.add_field(name="Nome:", value=titulo, inline=False)
                            emb = emb.add_field(name="Sinopse:", value=sinopse, inline=False)
                            emb = emb.set_footer(text="Kiniga.com - O limite é a sua imaginação")
                            emb = emb.set_image(url=img)
                            await ctx.message.delete()
                            await channel.send('',embed=emb)
                            await channel.send("\@everyone")
                            return 
                        except: 
                            return
                except:
                    return

def setup(client):
    client.add_cog(Noticia(client))
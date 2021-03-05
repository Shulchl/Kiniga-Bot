import discord
from discord.ext import commands
import discord.utils 
from discord.utils import get

class Role(commands.Cog, name='Cargos'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Cog de Cargos funcionando!       [√]')

    @commands.command(name='projeto', help='Recebe um determinado cargo ao digitar `&projeto <cargo> ou &projeto cargo @alguém`')
    @commands.has_any_role("Equipe", "Ajudante", "Moderador")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def projeto(self, ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        if not x:
            geth = discord.Embed(title='Erro!',description='Você precisa colocar algum cargo {}!\n'.format(member.mention),color=discord.Color.red())
            await ctx.send('',embed=geth)
        elif x:
            try: 
                novaRole = await ctx.guild.create_role(name='{}'.format(x))
                autorRole = discord.utils.get(ctx.guild.roles, name='{}'.format(novaRole))
                await member.add_roles(autorRole)
                geth = discord.Embed(title='Adicionado!',description='Seja bem vindo, {}! Agora você é autor!\n\n**{}**'.format(member.mention, autorRole.name),color=discord.Color.green())
                await ctx.send('',embed=geth)
            except:
                await ctx.send("Aconteceu alguma coisa errada... Mas eu não sei o que foi.")
        
    @commands.command(name='remover', help='Remover um cargo de sí mesmo ao digitar `&remover <cargo>`')
    @commands.has_any_role("Equipe", "Ajudante", "Moderador")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def remover(self, ctx, role: discord.Role, member: discord.Member = None):
        member = member or ctx.author
        x = ctx.message.content
        if not x:
            geth = discord.Embed(title='Erro!',description='Você precisa colocar algum cargo, {}!'.format(member.mention),color=discord.Color.red())
            await ctx.send('',embed=geth)
        elif x:
            await member.remove_roles(role)
            geth = discord.Embed(title='Removido!',description='Parece que hoje tivemos uma perda... A história {} foi removida do nosso site. \n\nEstaremos esperando o seu retorno, {}!'.format(role.name, member.mention),color=discord.Color.green())
            await ctx.send('',embed=geth)

def setup(client):
    client.add_cog(Role(client))
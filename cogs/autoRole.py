import discord, asyncio, re
from discord.ext import commands
import discord.utils 
from discord.utils import get
from discord.ext.commands.cooldowns import BucketType

class NoPrivateMessages(commands.CheckFailure):
    pass

def guild_only():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessages('Esse comando não pode ser usado em mensagens privadas!')
        return True
    return commands.check(predicate)


class Role(commands.Cog, name='Cargos'):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Categoria de Cargos funcionando!       [√]')

    ### TURN INTO AUTHOR

    @guild_only()         
    @commands.command(name='autor', help='Deletar história ao digitar `.autor <cargo> <usuário>` __(campo usuário é opcional)__ ')
    @commands.has_permissions(manage_roles=True)
    async def autor(self, ctx, role: discord.Role, member: discord.Member = None, reason=None):
        channel = ctx.guild.get_channel(831561655329751062)
        if ctx.message.channel == channel:
            member = member or ctx.author

            creatorRole = discord.utils.get(ctx.guild.roles, id=675027763412860969)
            autorRole   = discord.utils.get(ctx.guild.roles, id=667838759307575313)
            markRole    = discord.utils.get(ctx.guild.roles, id=837025056554090517)
            emb = discord.Embed(title='Tem certeza?',
                                description='Desejar tornar {} um autor?'.format(member.mention),
                                color=discord.Color.orange()).set_footer(text='Use a reação para confirmar')
            msg = await ctx.send('',embed=emb)
            await msg.add_reaction('✅')

            def check(reaction, member):
                return member == ctx.author and str(reaction.emoji) == '✅'

            try:
                await self.client.wait_for('reaction_add',timeout=20.0, check=check)
                for creatorRole in member.roles:
                    emb = discord.Embed(title='Hum...',
                                        description='Parece que o usuário já é autor.',
                                        color=discord.Color.blurple())
                    em = await ctx.send('',embed=emb)
                    await asyncio.sleep(5)
                    await msg.delete()
                    await em.delete()
                else:
                    roles = [creatorRole, autorRole, markRole]
                    member.add_roles(roles)
                    emb = discord.Embed(title='Parabéns!!',
                                        description='Agora você é autor, {}! Por favor, leia o fixado para saber como receber a TAG da sua história.'.format(member.mention),
                                        color=discord.Color.blurple())
                    await ctx.send('',embed=emb)
            except asyncio.TimeoutError:
                confirm = await ctx.send("Eu não recebi uma confirmação, que tal tentar de novo?")
                await msg.delete()
                await confirm.delete()
        else: return
    
    @autor.error
    async def autor_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            msg = await ctx.send("Você não tem permissão para usar este comando!")
            await asyncio.sleep(2)
            await msg.delete()
        elif isinstance(error, commands.BadArgument):
            msg = await ctx.send("Parece que essa história não existe!")
            await asyncio.sleep(2)
            await msg.delete()
        elif isinstance(error, commands.BotMissingPermissions):
            msg = await ctx.send("Parece que eu não tenho permissão para isso!")
            await asyncio.sleep(2)
            await msg.delete()
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(error)

#### GET PROJECT ROLE

    @guild_only()
    @commands.command(name='projeto', help='Recebe um determinado cargo ao digitar `.projeto <história> <usuário>` __(campo usuário é opcional)__ ')
    @commands.max_concurrency(1, per=BucketType.default, wait=False)
    @commands.has_any_role("Autor(a)", "Criador(a)", "Ajudante", "Equipe")
    async def projeto(self, ctx, role: discord.Role, member: discord.Member = None):
        channel = ctx.guild.get_channel(831561655329751062)
        markAuthorRole    = discord.utils.get(ctx.guild.roles, id=837020515004317707)
        if ctx.message.channel == channel:
            member = member or ctx.author
            role_id = role.id
            autorRole = discord.utils.get(ctx.guild.roles, id=role_id)
            eqpRole = discord.utils.get(ctx.guild.roles, name="Equipe")
            emb = discord.Embed(title='Opa!',
                                description='O cargo **{}** já existe, deseja adicioná-lo?!'.format(autorRole.mention),
                                color=discord.Color.orange()).set_footer(text='Use a reação para confirmar.')
            msg = await ctx.send('',embed=emb)
            await msg.add_reaction('✅')
            def check_ask(reaction, member):
                return member == ctx.author and str(reaction.emoji) == '✅'

            try:
                await self.client.wait_for('reaction_add',timeout=20.0, check=check_ask)
                aRole = []
                a_clean = []

                if role:
                    a = str(role)
                    a = a.replace('"', '')
                    a_clean = a
                    role_guild = discord.utils.get(ctx.guild.roles, name=a_clean)
                    if role_guild:
                        role_id = ctx.guild.get_role(int(role_guild.id))
                        aRole = role_id
                    else:
                        pass
                else:
                    await ctx.send("Você precisa digitar alguma coisa, meu querido.")
                    

                if aRole:
                    emb4 = discord.Embed(title='Opa!',
                                        description='Parece que {} já tem esse cargo.'.format(member.mention),color=discord.Color.green())
                    message = await ctx.send(embed=emb4)
                    await ctx.send(" ".join(message))
                    await asyncio.sleep(3)
                    await ctx.channel.purge(limit=2)
                    
                else:
                    emb = discord.Embed(title='Certo!',
                                        description='O cargo **{}** será recebido assim que algum ademir reagir à essa mensagem! 1'.format(autorRole.mention),
                                        color=discord.Color.orange())
                    msg = await ctx.send('',embed=emb)
                    await msg.add_reaction('✅')
                    def check_add(reaction, member):
                        return eqpRole in member.roles and str(reaction.emoji) == '✅'

                    try:
                        await self.client.wait_for('reaction_add',timeout=60.0, check=check_add)
                        await member.add_roles(autorRole, markAuthorRole)
                        emb4 = discord.Embed(title='Adicionado!',
                                            description='O cargo {} foi adicionado, e agora você é autor!.'.format(autorRole.mention), 
                                            color=discord.Color.green()).set_footer(text='Espero que seja muito produtivo escrevendo!')
                        await ctx.send('',embed=emb4)
                    except asyncio.TimeoutError:
                        emb5 = discord.Embed(title='Hum...',
                                            description='Eu não recebi uma confirmação de nenhum ademir, que tal tentar de novo?',color=discord.Color.blurple())
                        await ctx.send('',embed=emb5)
                        await asyncio.sleep(3)
                        await msg.delete()
            except asyncio.TimeoutError:
                emb5 = discord.Embed(title='Hum...',
                                    description='Eu não recebi uma confirmação, que tal tentar de novo?',
                                    color=discord.Color.blurple())
                await ctx.send('',embed=emb5)
                await asyncio.sleep(1)
                await ctx.channel.purge(limit=2)
        else:
            return

    @projeto.error
    async def projeto_error(self, ctx, error):
        if isinstance(error, commands.RoleNotFound):
            eqpRole = discord.utils.get(ctx.guild.roles, name="Equipe")
            markAuthorRole    = discord.utils.get(ctx.guild.roles, id=837020515004317707)
            #split the message into words
            string = str(ctx.message.content)
            temp = string.split()
            
            del temp[0] #Deleta cmd
            
            text = ' '.join(word for word in temp if not word.startswith('.') and not word.startswith('<')) #Cargo
            
            string_1 = str(ctx.message.content)
            temp_1 = string_1.split()
            
            del temp_1[0] #Deleta cmd2
            
            user = ' '.join(word for word in temp_1 if word.startswith('<')) #user
            
            member = []
            
            if user:
                a = str(user)
                a = a.replace("<","")
                a = a.replace(">","")
                a = a.replace("@","")
                a = a.replace("!","")
                user_guild = ctx.guild.get_member(int(a))
                member = user_guild
            else:
                member = ctx.author
            
            aRole = []
            a_clean = []
            
            if text:
                a = str(text)
                a = a.replace('"', '')
                a_clean = a
                role_guild = discord.utils.get(ctx.guild.roles, name=a_clean)
                if role_guild:
                    role_id = ctx.guild.get_role(int(role_guild.id))
                    aRole = role_id
                else:
                    pass
            else:
                await ctx.send("Você precisa digitar alguma coisa, meu querido.")
                
                
            emb = discord.Embed(title='Opa!',
                                description='O cargo **{}** será criado assim que algum ademir reagir à essa mensagem!'.format(a_clean),
                                color=discord.Color.orange())
            msg = await ctx.send('',embed=emb)
            await msg.add_reaction('✅')
            await asyncio.sleep(1)
            def check_create(reaction, member):
                return eqpRole in member.roles and reaction.message.id == msg.id and str(reaction.emoji) == '✅'
            try:
                await self.client.wait_for('reaction_add',timeout=60.0, check=check_create)
                if user:
                    if aRole:
                        emb = discord.Embed(title='Opa!',
                                            description='O cargo **{}** já existe, deseja adicioná-lo?!'.format(aRole),
                                            color=discord.Color.orange()).set_footer(text='Use a reação para confirmar.')
                        msg = await ctx.send('',embed=emb)
                        await msg.add_reaction('✅')
                        def check_ask(reaction, member):
                            return member == ctx.author and str(reaction.emoji) == '✅'
                            
                        try:
                            await self.client.wait_for('reaction_add',timeout=20.0, check=check_ask)
                            role_id = aRole.id
                            for role_id in member.roles:
                                emb4 = discord.Embed(title='Opa!',
                                                    description='Parece que {} já tem esse cargo.'.format(member.mention),
                                                    color=discord.Color.green())
                                message = await ctx.send(embed=emb4)
                                await ctx.send(" ".join(message))
                                await asyncio.sleep(3)
                                await ctx.channel.purge(limit=2)
                                
                            else:
                                emb = discord.Embed(title='Certo!',
                                                    description='O cargo **{}** será recebido assim que algum ademir reagir à essa mensagem! 1'.format(aRole),
                                                    color=discord.Color.orange())
                                msg = await ctx.send('',embed=emb)
                                await msg.add_reaction('✅')
                                def check_add(reaction, member):
                                    return eqpRole in member.roles and str(reaction.emoji) == '✅'
                                
                                try:
                                    await self.client.wait_for('reaction_add',timeout=60.0, check=check_add)
                                    await member.add_roles(aRole, markAuthorRole)
                                    channel = discord.utils.get(self.client.get_all_channels(), guild__name='Kiniga Brasil', name='regras')
                                    emb4 = discord.Embed(title='Adicionado!',
                                                        description='O cargo {} foi adicionado, e agora você é autor! \n Leia o canal {}.'.format(aRole, 
                                                                                                                                                    channel),
                                                        color=discord.Color.green()).set_footer(text='Espero que seja muito produtivo escrevendo!')
                                    await ctx.send('',embed=emb4)
                                except asyncio.TimeoutError:
                                    emb5 = discord.Embed(title='Hum...',
                                                        description='Eu não recebi uma confirmação de nenhum ademir, que tal tentar de novo?',
                                                        color=discord.Color.blurple())
                                    await ctx.send('',embed=emb5)
                                    await asyncio.sleep(3)
                                    await msg.delete()
                        except asyncio.TimeoutError:
                            emb5 = discord.Embed(title='Hum...',
                                                description='Eu não recebi uma confirmação, que tal tentar de novo?.',
                                                color=discord.Color.blurple())
                            await ctx.send('',embed=emb5)
                            await asyncio.sleep(2)
                            await ctx.channel.purge(limit=2)
                    else:
                        nRole = await ctx.guild.create_role(name=a_clean, reason="Nova história!")
                        await member.add_roles(nRole, markAuthorRole)
                        channel = discord.utils.get(self.client.get_all_channels(), guild__name='Testando bot', name='regras')
                        emb6 = discord.Embed(title='Criado!',
                                            description='{}, o cargo **{}** foi criado, e agora você é autor!'.format(member.mention, 
                                                                                                                      nRole.mention),
                                            color=discord.Color.green()).set_footer(text='Espero que seja muito produtivo escrevendo!')
                        await ctx.send('',embed=emb6)
                else:
                    if aRole:
                        emb = discord.Embed(title='Opa!',
                                            description='O cargo **{}** já existe, deseja adicioná-lo?!'.format(aRole),
                                            color=discord.Color.orange()).set_footer(text='Use a reação para confirmar.')
                        msg = await ctx.send('',embed=emb)
                        await msg.add_reaction('✅')
                        def check_ask(reaction, member):
                            return member == ctx.author and str(reaction.emoji) == '✅'
                            
                        try:
                            await self.client.wait_for('reaction_add',timeout=20.0, check=check_ask)
                            for role_id in member.roles:
                                emb4 = discord.Embed(title='Opa!',
                                                    description='Parece que {} já tem esse cargo.'.format(member.mention),
                                                    color=discord.Color.green())
                                await ctx.send(embed=emb4)
                                await asyncio.sleep(3)
                                await msg.delete()
                            else:
                                emb = discord.Embed(title='Certo!',
                                                    description='O cargo **{}** será recebido assim que algum ademir reagir à essa mensagem!'.format(aRole),
                                                    color=discord.Color.orange())
                                msg = await ctx.send('',embed=emb)
                                await msg.add_reaction('✅')
                                def check_add(reaction, member):
                                    return eqpRole in member.roles and str(reaction.emoji) == '✅'
                                
                                try:
                                    await self.client.wait_for('reaction_add',timeout=60.0, check=check_add)
                                    await member.add_roles(aRole, markAuthorRole)
                                    emb4 = discord.Embed(title='Adicionado!',
                                                        description='O cargo {} foi adicionado, e agora você é autor!'.format(aRole),
                                                        color=discord.Color.green()).set_footer(text='Espero que seja muito produtivo escrevendo!')
                                    await ctx.send('',embed=emb4)
                                except asyncio.TimeoutError:
                                    emb5 = discord.Embed(title='Hum...',
                                                        description='Eu não recebi uma confirmação de nenhum ademir, que tal tentar de novo?',
                                                        color=discord.Color.blurple())
                                    await ctx.send('',embed=emb5)
                                    await asyncio.sleep(3)
                                    await msg.delete()
                        except asyncio.TimeoutError:
                            emb5 = discord.Embed(title='Hum...',
                                                description='Eu não recebi uma confirmação, que tal tentar de novo?.',
                                                color=discord.Color.blurple())
                            await ctx.send('',embed=emb5)
                            await asyncio.sleep(2)
                            await ctx.channel.purge(limit=2)
                    else:
                        nRole = await ctx.guild.create_role(name=a_clean, reason="Nova história!")
                        await ctx.author.add_roles(nRole, markAuthorRole)
                        emb6 = discord.Embed(title='Criado!',
                                            description='{}, o cargo **{}** foi criado, e agora você é autor!'.format(ctx.author.mention, 
                                                                                                                      nRole.mention),
                                            color=discord.Color.green()).set_footer(text='Espero que seja muito produtivo escrevendo!')
                        await ctx.send('',embed=emb6)
                        
            except asyncio.TimeoutError:
                emb5 = discord.Embed(title='Hum...',
                                    description='Eu não recebi uma confirmação de nenhum ademir, que tal tentar de novo?',
                                    color=discord.Color.blurple())
                await ctx.send('',embed=emb5)
                await asyncio.sleep(3)
                await msg.delete()
                
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Já tem uma história na fila, você deve aguardar a sua vez.")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Parece que eu não tenho permissão para isso!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Parece que você não tenho permissão para isso!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(error)

### REMOVE PROJECT ROLE
  
    @guild_only()         
    @commands.command(name='r', help='Deletar história ao digitar `.r <cargo> <usuário>` __(campo usuário é opcional)__ ')
    @commands.has_permissions(manage_roles=True)
    async def r(self, ctx, role: discord.Role, member: discord.Member = None, reason=None):
        channel = ctx.guild.get_channel(831561655329751062)
        if ctx.message.channel == channel:
            member = member or ctx.author

            aRole = []
            a_clean = []

            if role:
                a = str(role)
                a = a.replace('"', '')
                a_clean = a
                role_guild = discord.utils.get(ctx.guild.roles, name=a_clean)
                if role_guild:
                    role_id = ctx.guild.get_role(int(role_guild.id))
                    aRole = role_id
                else:
                    pass
            else:
                await ctx.send("Você precisa digitar alguma coisa, meu querido.")

            #nomeRole = discord.utils.get(ctx.guild.roles, name=role)
            emb = discord.Embed(title='Tem certeza?',
                                description='Deseja realmente remover de {}?'.format(member.mention),
                                color=discord.Color.orange()).set_footer(text='Use a reação para confirmar')
            msg = await ctx.send('',embed=emb)
            await msg.add_reaction('✅')

            def check(reaction, member):
                return member == ctx.author and str(reaction.emoji) == '✅'

            try:
                await self.client.wait_for('reaction_add',timeout=20.0, check=check)
                if aRole:
                    await member.remove_roles(role)
                    emb = discord.Embed(title='?!',
                                        description='Deseja remover completamente? \nEssa ação não pode ser desfeita!',
                                        color=discord.Color.red()).set_footer(text='Use a reação para confirmar ou não reaja para cancelar.')
                    msg = await ctx.send('',embed=emb)
                    await msg.add_reaction('✅')

                    def check_delete(reaction, member):
                        return member == ctx.author and str(reaction.emoji) == '✅'

                    try:
                        await self.client.wait_for('reaction_add',timeout=10.0, check=check_delete)
                        await aRole.delete(reason="Hitória removida.")
                        await ctx.channel.purge(limit=4)
                        await asyncio.sleep(2)
                        emb2 = discord.Embed(title='História removida!',
                                            description='Espero que não se arrependa...',
                                            color=discord.Color.green())
                        await ctx.send('',embed=emb2)

                    except asyncio.TimeoutError:
                        emb3 = discord.Embed(title='Certo!',
                                            description='O cargo foi removido do usuário, mas não será removido completamente do servidor.',
                                            color=discord.Color.green())
                        await ctx.send('',embed=emb3)
                        await asyncio.sleep(5)
                        await ctx.channel.purge(limit=2)
                else:
                    emb = discord.Embed(title='Hum...',
                                        description='Parece que o usuário não tem esse cargo.',
                                        color=discord.Color.blurple())
                    await ctx.send('',embed=emb)
                    await asyncio.sleep(3)
                    await ctx.channel.purge(limit=2)
            except asyncio.TimeoutError:
                await ctx.send("Eu não recebi uma confirmação, que tal tentar de novo?")
                await asyncio.sleep(3)
                await ctx.channel.purge(limit=2)
        else: return
    
    @r.error
    async def r_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Você não tem permissão para usar este comando!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Parece que essa história não existe!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Parece que eu não tenho permissão para isso!")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(error)
        

def setup(client):
    client.add_cog(Role(client))

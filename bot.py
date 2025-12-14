import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
import asyncio

intents = discord.Intents.default()
intents.message_content = True   

bot = commands.Bot(command_prefix="!", intents=intents)


# Commande !ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Commande !userinfo
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    embed = discord.Embed(title=f"Informations sur {member.name}", color=discord.Color.blue())
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Nom", value=member.name)
    embed.add_field(name="Tag", value=member.discriminator)
    embed.add_field(name="Rôle principal", value=member.top_role.name)
    embed.add_field(name="Status", value=str(member.status))
    embed.set_thumbnail(url=member.avatar.url)
    await ctx.send(embed=embed)

# Commande !clear
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} messages supprimés.", delete_after=3)

# Commande !serverinfo
@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Informations sur le serveur {guild.name}", color=discord.Color.green())
    embed.add_field(name="Nom", value=guild.name)
    embed.add_field(name="ID", value=guild.id)
    embed.add_field(name="Nombre de membres", value=guild.member_count)
    embed.add_field(name="Nombre de canaux", value=len(guild.text_channels) + len(guild.voice_channels))
    embed.add_field(name="Région", value=guild.region)
    embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

# Commande !kick
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.name} a été expulsé pour {reason}.")

# Commande !ban
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.name} a été banni pour {reason}.")

# Commande !mute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, duration: str = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
        for channel in ctx.guild.text_channels:
            await channel.set_permissions(role, send_messages=False)
    await member.add_roles(role)
    if duration:
        await ctx.send(f"{member.name} est mute pendant {duration}.")
        # Délai pour unmute (par exemple, 10 minutes)
        await asyncio.sleep(600)  # 600 secondes = 10 minutes
        await member.remove_roles(role)
        await ctx.send(f"{member.name} n'est plus mute.")
    else:
        await ctx.send(f"{member.name} a été mute indéfiniment.")

# Commande !unmute
@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role:
        await member.remove_roles(role)
        await ctx.send(f"{member.name} a été unmute.")
    else:
        await ctx.send("Aucun rôle mute trouvé.")

# Commande !addrole
@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f"{role.name} a été ajouté à {member.name}.")

# Commande !removerole
@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f"{role.name} a été retiré de {member.name}.")

# Commande !roleinfo
@bot.command()
async def roleinfo(ctx, role: discord.Role):
    embed = discord.Embed(title=f"Informations sur le rôle {role.name}", color=role.color)
    embed.add_field(name="ID", value=role.id)
    embed.add_field(name="Mention", value=role.mention)
    embed.add_field(name="Couleur", value=role.color)
    embed.add_field(name="Permissions", value=', '.join([perm for perm, value in role.permissions if value]))
    await ctx.send(embed=embed)

# Commande !serverinvite
@bot.command()
async def serverinvite(ctx):
    invite = await ctx.channel.create_invite(max_uses=1, unique=True)
    await ctx.send(f"Voici un lien d'invitation temporaire pour le serveur : {invite}")

# Commande !invite
@bot.command()
async def invite(ctx):
    invite_url = "https://discord.com/oauth2/authorize?client_id=1449540215524950140&scope=268501217"
    await ctx.send(f"Voici le lien pour inviter le bot : {invite_url}")

# Commande !prefix
@bot.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, new_prefix: str):
    bot.command_prefix = new_prefix
    await ctx.send(f"Le préfixe du bot a été changé en `{new_prefix}`.")

# Commande !commands (remplace help)
@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Commandes du Bot", description="Voici une liste des commandes disponibles:", color=discord.Color.blue())
    embed.add_field(name="!ping", value="Vérifie si le bot répond.", inline=False)
    embed.add_field(name="!userinfo", value="Affiche des informations sur un utilisateur.", inline=False)
    embed.add_field(name="!clear", value="Supprime un nombre de messages spécifié.", inline=False)
    embed.add_field(name="!serverinfo", value="Affiche des informations sur le serveur.", inline=False)
    embed.add_field(name="!kick", value="Expulse un utilisateur du serveur.", inline=False)
    embed.add_field(name="!ban", value="Bannit un utilisateur du serveur.", inline=False)
    embed.add_field(name="!mute", value="Mute un utilisateur.", inline=False)
    embed.add_field(name="!unmute", value="Désactive le mute d'un utilisateur.", inline=False)
    embed.add_field(name="!addrole", value="Ajoute un rôle à un utilisateur.", inline=False)
    embed.add_field(name="!removerole", value="Retire un rôle à un utilisateur.", inline=False)
    embed.add_field(name="!roleinfo", value="Affiche des informations sur un rôle.", inline=False)
    embed.add_field(name="!serverinvite", value="Génère un lien d'invitation pour le serveur.", inline=False)
    embed.add_field(name="!invite", value="Génère un lien d'invitation pour le bot.", inline=False)
    embed.add_field(name="!prefix", value="Change le préfixe du bot.", inline=False)
    embed.add_field(name="!ltc", value="affiche l'adresse LTC.", inline=False)
    embed.add_field(name="!ppl", value="affiche le compte PayPal.", inline=False)
    embed.add_field(name="!ticket", value="Génere un embed pour ticket.", inline=False)
    embed.add_field(name="!roles", value="Génere un embed pour un role.", inline=False)
    await ctx.send(embed=embed)

# Commande !ppl (affiche le compte PayPal)
@bot.command()
async def ppl(ctx):
    await ctx.send("Voici mon compte PayPal : **ton.email@paypal.com**")

# Commande !ltc (affiche l'adresse LTC)
@bot.command()
async def ltc(ctx):
    await ctx.send("Voici mon adresse LTC : **LL8y783J7Qz6ZrzhBmKsiYVD9U66RTaFor**")

# Commande !ticket
@bot.command()
async def ticket(ctx):
    button = Button(label="Ouvrir un Ticket", style=ButtonStyle.green)

    async def button_callback(interaction):
        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="Tickets")

        if not category:
            category = await guild.create_category(name="Tickets")

        ticket_channel = await category.create_text_channel(
            f"ticket-{interaction.user.name}",
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True),
            }
        )

        embed = discord.Embed(title="Bienvenue dans ton Ticket", description="Décris ton problème ci-dessous, un modérateur viendra bientôt t'aider.", color=discord.Color.blue())
        embed.set_footer(text="Ticket créé par " + interaction.user.name)
        await ticket_channel.send(embed=embed)

        await interaction.response.send_message(f"Ton ticket a été créé ! Rendez-vous dans {ticket_channel.mention}", ephemeral=True)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    await ctx.send("Clique sur le bouton ci-dessous pour ouvrir un ticket", view=view)

# Commande !roles
@bot.command()
async def roles(ctx):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="Choisir rôle")
    if not category:
        category = await guild.create_category(name="Choisir rôle")

    roles = [".gg/vivastreet"]  # Liste des rôles disponibles à choisir

    buttons = []
    for role_name in roles:
        button = Button(label=role_name, style=ButtonStyle.primary, custom_id=role_name)
        async def role_button_callback(interaction, role_name=role_name):
            role = discord.utils.get(guild.roles, name=role_name)
            if role:
                await interaction.user.add_roles(role)
                await interaction.response.send_message(f"Tu as obtenu le rôle {role_name} !", ephemeral=True)
            else:
                await interaction.response.send_message(f"Le rôle {role_name} n'existe pas.", ephemeral=True)

        button.callback = role_button_callback
        buttons.append(button)

    view = View()
    for button in buttons:
        view.add_item(button)

    embed = discord.Embed(title="Choisis ton rôle", description="Clique sur un bouton ci-dessous pour choisir un rôle.", color=discord.Color.blue())
    await ctx.send(embed=embed, view=view)

# Lancer le bot avec ton token (remplace 'TON_TOKEN' par le token de ton bot)
bot.run("TTOKEN")

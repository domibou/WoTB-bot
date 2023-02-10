from bot import bot
import discord
import time
from datetime import datetime, timedelta
import asyncio
from random import randint

COLOR = 0x000000
delay_ended = True

@bot.command()
async def server(ctx):
    guild = ctx.guild
    top_roles = ""
    for i in [-1, -2, -3]:
        try:
            top_roles += f"{guild.roles[i].mention}"
        except:
            pass
    if guild.description:
        desc = guild.description
    else:
        desc = ""
    embed = discord.Embed(title=f'**{guild.name}**',
                            description=f"{desc}",
                            color=discord.Colour(COLOR)
                            )
    embed.add_field(name='**Members**', value=guild.member_count, inline=True)
    embed.add_field(name='**Creation**', value=guild.created_at.date(), inline=True)
    embed.add_field(name='**Level**', value=guild.premium_tier, inline=True)  
    embed.add_field(name='**Boosters**', value=guild.premium_subscription_count, inline=True)  
    embed.add_field(name='**Roles**', value=len(guild.roles), inline=True)
    embed.add_field(name='**Default role**', value=guild.default_role, inline=True)
    embed.add_field(name='**Top roles**', value=top_roles, inline=True)
    embed.set_thumbnail(url=guild.icon)
    embed.set_footer(text=guild.name, icon_url=guild.icon)

    await ctx.send(embed=embed)
    await ctx.send(await ctx.channel.create_invite())

@bot.command()
async def spam(ctx, member: discord.Member, *, message=None):
    global delay_ended
    can_do = True
    if can_do and delay_ended:
        if message is None:
            message = ''
        if len(message) > 50:
            await ctx.send('Make your message shorter')
        else:
            delay_ended = False
            n = 0
            while n < 10:
                await ctx.send(f'{member.mention} {message}')
                time.sleep(0.5)
                n += 1
            await asyncio.sleep(30)
            delay_ended = True
    else:
        if not delay_ended:
            await ctx.send("You are using spam too fast")

@bot.command()
async def poll(ctx, *, question):
    channel = ctx.message.channel
    embed = discord.Embed(title=f'**{question}**', description=ctx.message.author.mention, color=discord.Colour(COLOR))
    await ctx.send(embed=embed)
    await asyncio.sleep(0.5)
    async for i in channel.history(limit=1):
        await i.add_reaction('✅')
        await i.add_reaction('❌')

@bot.command()
async def rank(ctx, channel: discord.TextChannel):
    one_day = datetime.utcnow() - timedelta(days=1)
    names, msg = {}, 0

    async for i in channel.history(after=one_day, limit=20000):
        if i.author.name not in names:
            names[i.author.name] = 1
            msg += 1
        else:
            names[i.author.name] += 1
            msg += 1

    names = sorted(names.items(), key=lambda t: t[1])
    names.reverse()
    names = names[:5]
    rank_list = f"```css\n#{channel.name} - {msg} messages in the last day\n\n"

    for i in names:
        name = names[names.index(i)][0]
        percent = round((names[names.index(i)][1] / msg) * 100)
        rank = names.index(i) + 1
        spaces = 23 - (len(name) + len(str(percent)) + 3)
        spacing = spaces * '.'
        rank_list += f'{rank}. {name}{spacing}({percent}%)\n'
    rank_list += f"```"

    await ctx.send(rank_list)

@bot.command()
async def roles(ctx):
    guild = ctx.guild
    roles_list = "```fix\nName.........(created)\n\n"
    for i in reversed(guild.roles):
        if i.name == '@everyone':
            pass
        else:
            date = i.created_at.date().year
            spaces = 20 - (len(i.name) + len(str(date)))
            spacing = spaces * '.'
            roles_list += f'{i.name}{spacing}({date})\n'
    roles_list += "```"

    await ctx.send(roles_list)

@bot.command()
async def av(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author
    embed = discord.Embed(color=discord.Colour(COLOR))
    embed.set_image(url=member.avatar)
    embed.set_footer(text=member, icon_url=member.avatar)

    await ctx.send(embed=embed)

@bot.command()
async def profile(ctx, member: discord.Member = None, guild: discord.Guild = None):
    guild = ctx.guild if not guild else guild
    if member is None:
        member = ctx.message.author
    roles_list = ""
    for i in reversed(member.roles[1:]):
        roles_list += f'{i.mention}  '
    if member.nick is None:
        display = ''
    else:
        display = member.display_name

    guild_roles = [i.name for i in reversed(guild.roles[1:])]
    rank = guild_roles.index(str(member.top_role)) + 1

    embed = discord.Embed(title=f'**{member.name}**',
                            description=f'{display}',
                            color=discord.Colour(eval('0x' + str(member.color)[1:]))
                            )
    embed.set_thumbnail(url=member.avatar)
    embed.add_field(name='**Created**', value=member.created_at.date(), inline=True)
    embed.add_field(name='**Joined**', value=member.joined_at.date(), inline=True)
    embed.add_field(name=f'**Roles ({len(member.roles)-1})**', value=roles_list, inline=False)
    embed.add_field(name=f'**Hierarchy ({len(guild.roles)})**', value=f'{rank}', inline=False)
    embed.set_footer(text=member, icon_url=guild.icon)

    await ctx.send(embed=embed)

@bot.command()
async def boosters(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f'**Boosters** :moneybag:',
                            description=guild.name,
                            color=discord.Colour(COLOR)
                            )
    for booster in guild.premium_subscribers:
        embed.add_field(name=":heavy_minus_sign:", value=booster, inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title=':gear: **Commands**',
                            description=f"Prefix is {bot.command_prefix}\n[required]\n(optional)",
                            color=discord.Colour(COLOR)
                            )
    embed.set_thumbnail(url='https://i.imgur.com/y1xWylp.png')
    embed.add_field(name='`profile (@member)`', value='_member info_', inline=False)
    embed.add_field(name='`server`', value='_server info_', inline=False)
    embed.add_field(name='`stats [name]`', value='_player stats_', inline=False)
    embed.add_field(name='`clan [region] [name]`', value='_clan stats_', inline=False)
    embed.add_field(name='`wr [player]`', value='_recent stats_', inline=False)
    embed.add_field(name='`rating`', value='_rating battles leaderboard_', inline=False)
    embed.add_field(name='`av (@member)`', value="_avatar_", inline=False)
    embed.add_field(name='`rank [channel]`', value='_most messages (1 day)_', inline=False)
    embed.add_field(name='`poll [question]`', value="_quick poll_", inline=False)
    embed.add_field(name='`spam [@member] (message)`', value="_spam people_", inline=False)
    embed.add_field(name='`roles`', value='_server roles info_', inline=False)
    embed.add_field(name='`pro`', value='_gamer moments_', inline=False)
    embed.add_field(name='`bad`', value='_embarassing clips_', inline=False)
    
    await ctx.send(embed=embed)
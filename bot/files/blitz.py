from bot import bot
import discord
from random import randint
import requests

app_id = 'secret'
TOKEN = 'secret'

imgurClient = "edea664f0fb59b7"
good_album = "Yt4DsBn"
bad_album = "R65ls0r"
COLOR = 0x000000

@bot.command()
async def clan(ctx, region, *, tag):
    if region == 'na' or 'NA':
        region = 'com'
    try:
        r = requests.get(f'https://api.wotblitz.{region}/wotb/clans/list/?application_id=c918d11439e90d31acbbc2f245754c4c&search={tag}').json()
        clan_id = str(r["data"][0]["clan_id"])
    except:
        await ctx.send('Clan not found')

    r = requests.get(f'https://api.wotblitz.{region}/wotb/clans/info/?application_id=c918d11439e90d31acbbc2f245754c4c&clan_id={clan_id}').json()

    name = r["data"][clan_id]["name"]
    tag = r["data"][clan_id]["tag"]
    members_count = r["data"][clan_id]["members_count"]
    leader_name = r["data"][clan_id]["leader_name"]
    creator_name = r["data"][clan_id]["creator_name"]
    motto = r["data"][clan_id]["motto"]
    description = r["data"][clan_id]["description"]
    clan_member_ids = []
    clan_wins = clan_battles = clan_dmg = pro_player_count = pro_count = 0
    emblem_id = r["data"][clan_id]["emblem_set_id"]
    color = [0xE6E6E6, 0x289C26, 0x0032FF, 0x6000BF, 0xF2B600]

    for i in r["data"][clan_id]["members_ids"]:
        clan_member_ids.append(str(i))
    for i in clan_member_ids:
        r = requests.get(f'https://api.wotblitz.com/wotb/account/info/?application_id=c918d11439e90d31acbbc2f245754c4c&account_id={i}').json()
        if r["data"][i] == None:
            pass
        else:
            clan_battles += int(r["data"][i]["statistics"]["all"]["battles"])
            clan_wins += int(r["data"][i]["statistics"]["all"]["wins"])
            clan_dmg += int(r["data"][i]["statistics"]["all"]["damage_dealt"])
    clan_wr = round((clan_wins / clan_battles) * 100, 2)
    clan_avg_dmg = str(round(clan_dmg / clan_battles))

    if clan_wr <= 49.99:
        Color = color[0]
    elif 50.00 <= clan_wr <= 59.99:
        Color = color[1]
    elif 60.00 <= clan_wr <= 69.99:
        Color = color[2]
    elif 70.00 <= clan_wr <= 100.00:
        Color = color[3]

    for i in clan_member_ids:
        r = requests.get(f'https://api.wotblitz.com/wotb/account/achievements/?application_id=c918d11439e90d31acbbc2f245754c4c&account_id={i}').json()
        try:
            if r["data"][i]["achievements"]["medalTournamentProfessional"] > 0:
                pro_player_count += 1
                pro_count += int(r["data"][i]["achievements"]["medalTournamentProfessional"])
        except:
            pass

    if pro_player_count >= 7:
        Color = color[4]

    embed = discord.Embed(title=f'**{name} [{tag}]**', description=f'_{motto}_', color=discord.Colour(Color))
    embed.set_thumbnail(url=f'https://wotblitz-gc.gcdn.co/icons/clanEmblems1x/clan-icon-v2-{emblem_id}.png')
    embed.add_field(name='**Winrate**', value=f'{clan_wr}%')
    embed.add_field(name='**Damage**', value=clan_avg_dmg)
    embed.add_field(name='**Members**', value=members_count)
    embed.add_field(name='**Leader**', value=leader_name)
    if pro_player_count > 0:
        embed.add_field(name='**Pro players**', value=f'{pro_player_count} ({pro_count} medals)')
    embed.add_field(name='**Creator**', value=creator_name)
    embed.set_footer(text=tag, icon_url=f'https://wotblitz-gc.gcdn.co/icons/clanEmblems1x/clan-icon-v2-{emblem_id}.png')

    await ctx.send(f'```\n{description}\n```')
    await ctx.send(embed=embed)

@bot.command()
async def wr(ctx, player):
    r = requests.get(f'https://api.wotblitz.com/wotb/account/list/?application_id=c918d11439e90d31acbbc2f245754c4c&search={player}').json() #_________wotblitz.com data___________
    account_id = str(r["data"][0]["account_id"])
    r = requests.get(f'https://api.wotblitz.com/wotb/account/info/?application_id=c918d11439e90d31acbbc2f245754c4c&account_id={account_id}').json()
    nickname = str(r["data"][account_id]["nickname"])
    r = requests.get(f'https://na.wotblitz.com/en/api/player-profile/players/{account_id}/').json()

    try:
        r = requests.get(f'https://api.wotblitz.com/wotb/clans/accountinfo/?application_id=c918d11439e90d31acbbc2f245754c4c&account_id={account_id}').json()
        clan_id = str(r["data"][account_id]["clan_id"])
        r = requests.get(f'https://api.wotblitz.com/wotb/clans/info/?application_id=c918d11439e90d31acbbc2f245754c4c&clan_id={clan_id}').json()
        tag = str(r["data"][clan_id]["tag"])
    except:
        tag = None

    r = requests.get(f'https://www.blitzstars.com/api/top/player/{account_id}').json() #_________blitzstars.com data___________
    try:
        recent_wr = str(round(r["period30d"]["special"]["winrate"], 2))
        wn8 = str(round(r["period30d"]["wn8"]))
        avg_dmg = str(round(r["period30d"]["special"]["dpb"]))
        avg_tier = str(round(r["period30d"]["avg_tier"], 2))
        battles = str(round(r["period30d"]["all"]["battles"]))
    except KeyError:
        await ctx.send("No 30 day stats recorded")

    wn8_color = [0x8002d8, 0xB700BF, 0x0051FF, 0x4099BF, 0x4D7326, 0x76A731, 0xE6CE00, 0xCC7A00, 0xCD3333, 0x930D0D]
    wr_color = [':white_circle:', ':green_circle:', ':blue_circle:', ':purple_circle:']

    if int(wn8) <= 299:
        color2 = wn8_color[9]
    elif 300 <= int(wn8) <= 449:
        color2 = wn8_color[8]
    elif 450 <= int(wn8) <= 649:
        color2 = wn8_color[7]
    elif 650 <= int(wn8) <= 899:
        color2 = wn8_color[6]
    elif 900 <= int(wn8) <= 1199:
        color2 = wn8_color[5]
    elif 1200 <= int(wn8) <= 1599:
        color2 = wn8_color[4]
    elif 1600 <= int(wn8) <= 1999:
        color2 = wn8_color[3]
    elif 2000 <= int(wn8) <= 2449:
        color2 = wn8_color[2]
    elif 2450 <= int(wn8) <= 2899:
        color2 = wn8_color[1]
    elif int(wn8) >= 2900:
        color2 = wn8_color[0]

    embed = discord.Embed(title=f'**Recent stats**', description=f'Last **{battles}** battles', color=discord.Colour(color2))
    embed.add_field(name='**WN8**', value=wn8)
    embed.add_field(name='**Winrate**', value=f'{recent_wr}%')
    embed.add_field(name='**Damage**', value=avg_dmg)
    embed.add_field(name='**Avg tier**', value=avg_tier)
    if tag != None:
        embed.set_footer(text=f'{nickname} [{tag}]', icon_url=ctx.guild.icon)
    else:
        embed.set_footer(text=f'{nickname}', icon_url=ctx.guild.icon)

    await ctx.send(embed=embed)

@bot.command()
async def stats(ctx, player):
    r = requests.get(f'https://api.wotblitz.com/wotb/account/list/?application_id=c918d11439e90d31acbbc2f245754c4c&search={player}').json()
    account_id = str(r["data"][0]["account_id"])

    try:
        clan_id = str(r["data"][account_id]["clan_id"])
        r = requests.get(f'https://api.wotblitz.com/wotb/clans/info/?application_id=c918d11439e90d31acbbc2f245754c4c&clan_id={clan_id}').json()
        tag = str(r["data"][clan_id]["tag"])
    except:
        tag = None

    r = requests.get(f'https://api.wotblitz.com/wotb/account/info/?application_id=c918d11439e90d31acbbc2f245754c4c&account_id={account_id}').json()
    
    nickname = str(r["data"][account_id]["nickname"])
    battles = str(r["data"][account_id]["statistics"]["all"]["battles"])
    max_xp_tank_id = str(r["data"][account_id]["statistics"]["all"]["max_xp_tank_id"])
    wins = str(r["data"][account_id]["statistics"]["all"]["wins"])
    damage_dealt = str(r["data"][account_id]["statistics"]["all"]["damage_dealt"])
    damage_received = str(r["data"][account_id]["statistics"]["all"]["damage_received"])
    max_xp = str(r["data"][account_id]["statistics"]["all"]["max_xp"])
    hits = str(r["data"][account_id]["statistics"]["all"]["hits"])
    shots = str(r["data"][account_id]["statistics"]["all"]["shots"])
    frags = str(r["data"][account_id]["statistics"]["all"]["frags"])
    
    wr = str(round((eval(wins) / eval(battles)) * 100, 2))
    dr = str(round(eval(damage_dealt) / eval(damage_received), 2))
    dmg = str(round(eval(damage_dealt) / eval(battles)))
    hitrate = str(round((eval(hits) / eval(shots)) * 100, 2))
    avg_xp = str(round(r["data"][account_id]["statistics"]["all"]["xp"] / int(battles)))
    kpb = str(round(int(frags) / int(battles), 2))

    r = requests.get(f'https://api.wotblitz.com/wotb/tanks/stats/?application_id=c918d11439e90d31acbbc2f245754c4c&account_id={account_id}').json()

    tank_list = r["data"][account_id]
    tanks = []
    
    for i in range(len(tank_list)):
        if tank_list[i]["all"]["battles"] >= 100:
            damage = round(tank_list[i]["all"]["damage_dealt"] / tank_list[i]["all"]["battles"])
            id = tank_list[i]["tank_id"]
            tanks.append([damage, id])

    best_id = str(list(reversed(sorted(tanks)))[0][1])
    secondbest_id = str(list(reversed(sorted(tanks)))[1][1])
    thirdbest_id = str(list(reversed(sorted(tanks)))[2][1])
    best_dmg = int(list(reversed(sorted(tanks)))[0][0])
    secondbest_dmg = int(list(reversed(sorted(tanks)))[1][0])
    thirdbest_dmg = int(list(reversed(sorted(tanks)))[2][0])

    nations = {"usa": ":flag_us:", "germany": ":flag_de:", "ussr": ":flag_ru:", "uk": ":flag_gb:",
                "japan": ":flag_jp:", "china": ":flag_cn:", "france": ":flag_fr:", "european": ":flag_eu:",
                "other": ":black_small_square:"}

    max_xp_tank = best_name = secondbest_name = thirdbest_name = "(Missing)"
    try:
        r = requests.get(f'https://api.wotblitz.com/wotb/encyclopedia/vehicles/?application_id=c918d11439e90d31acbbc2f245754c4c&tank_id={max_xp_tank_id}').json()  # _____________Max xp tank_____________
        max_xp_tank = str(r["data"][max_xp_tank_id]["name"])
    except:
        pass
    try:
        r = requests.get(f'https://api.wotblitz.com/wotb/encyclopedia/vehicles/?application_id=c918d11439e90d31acbbc2f245754c4c&tank_id={best_id}').json()
        best_name = str(r["data"][best_id]["name"])
        best_nation = str(r["data"][best_id]["nation"])
        best_flag = nations[best_nation]
    except:
        pass
    try:
        r = requests.get(f'https://api.wotblitz.com/wotb/encyclopedia/vehicles/?application_id=c918d11439e90d31acbbc2f245754c4c&tank_id={secondbest_id}').json()
        secondbest_name = str(r["data"][secondbest_id]["name"])
        secondbest_nation = str(r["data"][secondbest_id]["nation"])
        secondbest_flag = nations[secondbest_nation]
    except:
        pass
    try:
        r = requests.get(f'https://api.wotblitz.com/wotb/encyclopedia/vehicles/?application_id=c918d11439e90d31acbbc2f245754c4c&tank_id={thirdbest_id}').json()
        thirdbest_name = str(r["data"][thirdbest_id]["name"])
        thirdbest_nation = str(r["data"][thirdbest_id]["nation"])
        thirdbest_flag = nations[thirdbest_nation]
    except:
        pass

    r = requests.get(f'https://api.wotblitz.com/wotb/account/achievements/?application_id=c918d11439e90d31acbbc2f245754c4c&account_id={account_id}').json()  # _____________Achievements_____________
    
    try:
        aces = str(r["data"][account_id]["achievements"]["markOfMastery"])
        aces_percent = round((float(aces) / int(battles)) * 100, 2)
    except:
        aces = aces_percent = '0'
    try:
        top_gun = str(r["data"][account_id]["achievements"]["mainGun"])
        top_gun_percent = round((float(top_gun) / int(battles)) * 100, 2)
    except:
        top_gun = top_gun_percent = '0'
    try:
        ras = str(r["data"][account_id]["achievements"]["heroesOfRassenay"])
    except:
        ras = '0'
    try:
        kolo = str(r["data"][account_id]["achievements"]["medalKolobanov"])
    except:
        kolo = '0'

    pro = False
    color = [0xE6E6E6, 0x289C26, 0x0032FF, 0x6000BF, 0xF2B600]
    
    try:
        if r["data"][account_id]["achievements"]["medalTournamentProfessional"] > 0:
            pro = True
            color = color[4]
    except:
        if float(wr) <= 49.99:
            color = color[0]
        elif 50.00 <= float(wr) <= 59.99:
            color = color[1]
        elif 60.00 <= float(wr) <= 69.99:
            color = color[2]
        elif 70.00 <= float(wr) <= 100.00:
            color = color[3]

    if tag is not None:
        embed = discord.Embed(title=f"**{nickname} [{tag}]**", description="**Player stats**", color=discord.Colour(color))  # _____________Embed_____________
        embed.set_footer(text=f'{nickname} [{tag}]', icon_url=ctx.guild.icon)
    else:
        embed = discord.Embed(title=f"**{nickname}**", description="_Player stats_", color=discord.Colour(color))
        embed.set_footer(text=f'{nickname}', icon_url=ctx.guild.icon)

    embed.add_field(name='**Battles**', value=battles)
    embed.add_field(name='**Winrate**', value=f'{wr} %')
    embed.add_field(name='**Damage**', value=dmg)
    embed.add_field(name='**XP**', value=avg_xp)
    embed.add_field(name='**Damage ratio**', value=dr)
    embed.add_field(name='**KPB**', value=kpb)
    embed.add_field(name='**Accuracy**', value=f'{hitrate} %')
    embed.add_field(name='**Max XP**', value=f'{max_xp} ({max_xp_tank})')
    embed.add_field(name='**Top tanks (dmg)**', value=f'{best_flag}{best_name}, **{best_dmg}**\n{secondbest_flag}{secondbest_name}, **{secondbest_dmg}**\n{thirdbest_flag}{thirdbest_name}, **{thirdbest_dmg}**')
    embed.add_field(name='**Achievements**', value=f'Aces: **{aces}** ({aces_percent} %)\nTop gun: **{top_gun}** ({top_gun_percent} %)\nKolobanov: **{kolo}**\nRaseiniai: **{ras}**')
    if pro:
        embed.set_thumbnail(url='https://i.imgur.com/DVTHHTu.png')

    await ctx.send(embed=embed)

@bot.command()
async def rating(ctx):
    board = "```css\nRating Battles\n\n"
    r = requests.get("https://na.wotblitz.com/en/api/rating-leaderboards/league/0/top/").json()
    for i in r["result"]:
        name = i["nickname"]
        tag = i["clan_tag"]
        score = i["score"]
        position = i["number"]
        spaces = 25 - (len(name) + len(tag))
        spacing = spaces * '.'
        board += f'{position}. [{tag}]{name}{spacing}{score}\n'
    board += "```"

    await ctx.send(board)

@bot.command()
async def pro(ctx):
    url = f"https://api.imgur.com/3/album/{pro_album}/images"
    payload={}
    files={}
    headers = {'Authorization': f'Client-ID {imgurClient}'}
    r = requests.request("GET", url, headers=headers, data=payload, files=files).json()
    index = randint(0, len(r["data"])-1)
    await ctx.send(r["data"][index]["link"])

@bot.command()
async def bad(ctx):
    url = f"https://api.imgur.com/3/album/{bad_album}/images"
    payload={}
    files={}
    headers = {'Authorization': f'Client-ID {imgurClient}'}
    r = requests.request("GET", url, headers=headers, data=payload, files=files).json()
    index = randint(0, len(r["data"])-1)
    await ctx.send(r["data"][index]["link"])


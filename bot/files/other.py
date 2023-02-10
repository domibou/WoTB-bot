from bot import bot
from discord.ext.commands import is_owner
import time
from imgurpython import ImgurClient

imgurClient = "secret"
imgurClientSecret = "secret"
pro_album = "Yt4DsBn"
bad_album = "R65ls0r"

bot_users = 0

@is_owner()
async def servers(ctx):
    guilds = "```css\n"
    for i in bot.guilds:
        spaces = 25 - (len(i.name) + 2 + len(str(i.member_count)))
        spacing = spaces * '.'
        guilds += f'{i.name}{spacing}({i.member_count})\n'
    guilds += '```'
    await ctx.send(guilds)
    
@bot.command()
async def add(ctx, album):
    if album == "pro":
        album = pro_album
    elif album == "bad":
        album = bad_album

    client = ImgurClient(imgurClient, imgurClientSecret)
    authorization_url = client.get_auth_url("pin")
    await ctx.send(authorization_url)
    time.sleep(12)
    channel = ctx.message.channel
    async for message in channel.history(limit=1):
                pin = str(message.content)
    credentials = client.authorize(pin, 'pin')
    client.set_user_auth(credentials['access_token'], credentials['refresh_token'])
    config = {"album": album}                                  
    await ctx.send("clip added")

@bot.command()
async def solve(ctx, *, equation):
    safe_list = "123456789(-sctlpe"
    functions = ["sin", "cos", "tan", "sqrt", "log", "pi", "e"]
    if equation[0] in safe_list:
        for i in equation:
            if i == '^' or i == 'x':
                equation = equation.replace('^', '**')
                equation = equation.replace('x', '*')
        for foo in functions:
            if foo in equation:
                equation = equation.replace(foo, f'math.{foo}')
        block = "```\n"
        block += f'{str(eval(equation))}\n'
        block += "```"
        await ctx.send(block)

@bot.command()
async def itg(ctx, coef, exp, a, b):
    coef, exp, a, b = float(coef), float(exp), float(a), float(b)
    i = (coef * (b ** (exp + 1)) / (exp + 1)) - (coef * (a ** (exp + 1)) / (exp + 1))
    await ctx.send(f'∫ f(x)dx = {i}')

@bot.event
async def on_command_completion(ctx):
    global bot_users
    if ctx.message.author.id != 283057824010076173:
        bot_users += 1

@is_owner()
async def users(ctx):
    await ctx.send(f"```fix\n{bot_users}\n```")

@is_owner()
async def clear(ctx):
    global bot_users
    bot_users = 0
    await ctx.send("users cleared")
    



        


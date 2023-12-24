import random
import discord

import mysql.connector
from discord.ext import commands

client = commands.Bot(intents=discord.Intents.all(), command_prefix="~")

mydb=mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='bancatransilvania'
)
client.db = mydb
# cursor object
cursor_obj = client.db.cursor(dictionary=True)

class rolls:
    def __init__(self, value, collum, half, section):
        self.value=value
        self.collum=collum
        self.half=half
        self.section=section

roullete=[]
colum = 0
for i in range(0, 37):
    val = i;
    if val == 0:
        roullete.append(rolls(val, 0, 'null', 'null'))
        colum += 1
    else:
        if val > 0 and val <= 12:
            _half = 'first'
            sector = 'one'
        elif val > 12 and val <= 24:
            if val<=18:
                _half = 'first'
                sector = 'two'
            else:
                _half = 'second'
                sector = 'two'
        else:
            _half = 'second'
            sector = 'three'
        roullete.append(rolls(val, colum, _half, sector))
        if i % 3 == 0:
            colum += 1

@client.event
async def on_ready():
    print("bot is ready")
    for obj in roullete:
        print(obj.value,obj.collum,obj.half,obj.section)


@client.command()
async def create(ctx):
    members=ctx.message.guild.members#e nevoie de un try catch dar mai tarziu
    for members in members:
        print(members.name)
        addTo_Database(members.name,members.id,100)


def addTo_Database(name,id,money):
    query="INSERT INTO bancatransilvania(userID, userName, wallet) VALUES (%s, %s, %s)"
    values=(id,name,100)
    cursor_obj.execute(query,values)
    client.db.commit()
    print(id, 'added')

@client.command()
async def hello(ctx):
    await ctx.send("天上太阳红呀红彤彤诶心中的太阳是毛泽东诶他领"
                   "导我们得解放诶人民翻身当家做主人咿呀咿吱呦喂呀而"
                   "呀吱呦啊人民翻身当家做主人天上太阳红呀红彤彤诶心中"
                   "的太阳是毛泽东诶他领导我们奋勇向前进诶革命江山一耶一片红诶咿呀咿吱呦喂"
                   "呀而呀吱呦啊13"
                   "革命江山一片红(诶)")

@client.command()
async def check_balance(ctx):
    await ctx.send("test")
    cursor_obj.execute(f"SELECT * FROM bancatransilvania WHERE userID = {ctx.author.id}")
    myresult = cursor_obj.fetchall()
    for row in myresult:
        await ctx.send(f"{ctx.author.name} are {row['wallet']}")

def modify(money,id,type):
    cursor_obj.execute(f"SELECT * FROM bancatransilvania WHERE userID = {id}")
    myresult = cursor_obj.fetchall()
    for row in myresult:
        new_wallet=int(row['wallet'])
    if type == "extract":
        new_wallet -= money
        cursor_obj.execute(f"UPDATE bancatransilvania SET wallet={new_wallet} WHERE userID = {id}")
        client.db.commit()
    elif type == "add":
        new_wallet += money
        cursor_obj.execute(f"UPDATE bancatransilvania SET wallet={new_wallet} WHERE userID = {id}")
        client.db.commit()


@client.command()
async def info_commands(ctx):
    await ctx.send("Available commands: ~check_balance, ~hello")

@client.command()
async def test(ctx):
    await ctx.send("test")

@client.command()
async def play_barbut(ctx,args=None):
    if args != None:
        if not args.isnumeric():
            await ctx.send("You have not provided an integer")
        else:
            bet = int(args)
            member=ctx.author
            await ctx.send(f"You are betting {bet} stanobani.Do you choose higher/lower")
            while True:
                message=await client.wait_for('message',check=lambda message:message.author==member)
                if "higher" in message.content:
                    await ctx.send("test higher good")
                    await barbut(ctx,1, bet)
                    return
                else:
                    if "lower" in message.content:
                        await ctx.send("test lower good")
                        await barbut(ctx, -1, bet)
                        return
                    else:
                        await ctx.send("Invalid command")
                        return
            else:
                await ctx.send(f"Please insert your bet")

async def barbut(ctx, key, money):
        rolls1 = random.randint(1, 6)
        rolls2 = random.randint(1, 6)
        score = rolls1 + rolls2
        player_rolls1 = random.randint(1, 6)
        player_rolls2 = random.randint(1, 6)
        if score * key > (player_rolls2 + player_rolls1) * key:
            await ctx.send(f"My rolls {rolls1}, {rolls2} , your rolls: {player_rolls2}, {player_rolls1}")
            await ctx.send(f"My score: {score}, your score {player_rolls2 + player_rolls1}")
            await ctx.send(f"Bozo you lost get gud")
            modify(money, ctx.author.id, "extract")
        else:
            if score * key < (player_rolls2 + player_rolls1) * key:
                await ctx.send(f"My rolls {rolls1} {rolls2} , your rolls: {player_rolls2}, {player_rolls1}")
                await ctx.send(f"My score: {score}, your score {player_rolls2 + player_rolls1}")
                await ctx.send(f"bulan you won")
                modify(money, ctx.author.id, "add")
            else:
                await ctx.send(f"My rolls {rolls1} {rolls2} , your rolls: {player_rolls2}, {player_rolls1}")
                await ctx.send(f"My score: {score}, your score {player_rolls2 + player_rolls1}")
                await ctx.send(f"Draw :sleepy: ")

@client.command()
async def play_roullete(ctx,args=None):
    if args != None:
        if not args.isnumeric():
            await ctx.send("You have not provided an integer")
        else:
            bet = int(args)
            member = ctx.author
            await ctx.send(file=discord.File("roullete.jpg"))
            await ctx.send(f"You are betting {bet} stanobani.If you want to continue type your bet, "
                           f"or if you want to cancel, press cancel \n"
                           f"To place your bet, write like this: _value_bet(a number from 0 to 36) | _pair(even/odd) _half"
                           f"(first/second) _sector(one,two,three). \n"
                           f"It's not neccesary to write all of them.You can bet only on pair, or on half and pair.YOU CAN'T"
                           f" BET ON OTHER CRITERIAS IF YOU START YOUR BET WITH VALUE!")
            await ctx.send(f"Prices:\n 1.On value you get 3.5x the sum you bet on \n"
                           f"2.On pair and halfs you get 100% the sum you bet on \n"
                           f"3.On sector you get 115% the sum you bet on"
                           f"4.If you betted on more criterias, the wins adds up.(Max 315% of the sum you bet on")
            while True:
                message = await client.wait_for('message', check=lambda message: message.author == member)
                roll=random.randint(0,37);
                print(message.content)
                object=roullete[roll]
                if "cancel" in message.content:
                    await ctx.send("Canceled")
                    return
                #await ctx.send(f"The number pulled {object.value}, half: {object.half}, sector: {object.section}")
                if message.content.isnumeric():
                    if object.value==int(message.content):
                        await ctx.send(f"bulan you won")
                        modify(bet,ctx.author.id,"add")
                        return
                    else:
                        await ctx.send( f"The number pulled {object.value}, half: {object.half}, sector: {object.section}")
                        await ctx.send(f"The number was {object.value}. L bozo u lost")
                        modify(bet,ctx.author.id,"extract")
                        return
                else:
                    total_price=0
                    if (await check_parity(ctx, message, object)==False) or (await check_half(ctx, message, object)==False) \
                            or (await check_sector(ctx, message, object)==False):
                        await ctx.send(f"The number pulled {object.value}, half: {object.half}, sector: {object.section}")
                        await ctx.send(f"The number was {object.value}. L bozo u lost")
                        return
                    elif (await check_parity(ctx, message, object)==-1) and (await check_half(ctx, message, object)==-1) \
                            and (await check_sector(ctx, message, object)==-1):
                        await ctx.send(f"Invalid command")
                        return
                    else:
                        if await check_parity(ctx, message, object)==True:
                            total_price+=bet
                        if await check_half(ctx, message, object)==True:
                            total_price+=bet
                        if await check_sector(ctx, message, object)==True:
                            total_price+=int(bet*115/110)
                        await ctx.send(f"The number pulled {object.value}, half: {object.half}, sector: {object.section}")
                        await ctx.send(f"bulan you won {total_price} stanokeni")
                        return



async def check_parity(ctx, message, roll):
    parity=roll.value%2
    if "even" in message.content:
        if parity==0:
            return True
        else:
            return False
    elif "odd" in message.content:
        if parity!=0:
            return True
        else:
            return False
    else:
        return -1 #-1 null command


async def check_half(ctx, message, roll):
    if "first" in message.content:
        if roll.half=="first":
            return True
        else:
            return False
    elif "second" in message.content:
        if roll.half=="second":
            return True
        else:
            return False
    else:
        return -1

async def check_sector(ctx, message, roll):
    if "one" in message.content:
        if roll.section == "one":
            return True
        else:
            return False
    elif "two" in message.content:
        if roll.section == "two":
            return True
        else:
            return False
    elif "three" in message.content:
        if roll.section == "three":
            return True
        else:
            return False
    else:
        return -1

@client.command()
async def black_jack(ctx, args=None):
    print("mai tarziu")


client.run('token')
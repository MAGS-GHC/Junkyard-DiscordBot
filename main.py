from discord.ext import commands
import discord
import random
import json
import datetime


import os

TOKEN="MTEwMjUwODQ0Mzc5NDk0ODIwNg.GdETCf.moH5j0d8vDk45lQ4JkJH9APGNHo5jKvGC2s3ug"
CLIENT=1102839933896503325

#### Valg af Prefix ####
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

################### Random Commands ####################################
@bot.event
async def on_ready():    
    print('Bot er online')
    channel = bot.get_channel(CLIENT)
    #await channel.send("Hello World!")


@bot.command()
async def default(ctx):
    await ctx.send('Hello World!')
################### Random Commands ####################################


################### Economy Commands ####################################
@bot.command()
async def balance(ctx):
    channel = bot.get_channel(CLIENT)

    
    await open_account(ctx.author)

    users = await get_bank_data()

    wallet_amt = users[str(ctx.author.name)]["wallet"]

    ### EVT: forkorte id/lave custom id.
   ## await channel.send(f'Your ID: {ctx.author.name}')


    em = discord.Embed(title = f'{ctx.author.name}s balance', color = discord.Color.blue())
    em.add_field(name = 'Wallet',value = (f'{wallet_amt} gold'))
    await ctx.send(embed = em)

async def open_account(user):


    users = await get_bank_data()

    if str(user.name) in users:
        return False
    else: 
        users[str(user.name)] = {'wallet':1000} 

    with open('wallet.json', 'w') as file:
        json.dump(users,file)
        return True 


async def get_bank_data():
    with open('wallet.json', 'r') as file:
        users = json.load(file)
        return users

@bot.command()
async def gift(ctx, amount: int, friend: discord.Member):
    users = await get_bank_data()
    author_name = str(ctx.author.name)
    friend_name = str(friend.name)

    if author_name not in users:
        await open_account(ctx.author)

    if friend_name not in users:
        await open_account(friend)

    if amount < 0:
        await ctx.send("You cant gift less that 1 gold")
        return
    
    wallet_amt  = users[author_name]["wallet"]

    if wallet_amt < amount:
        await ctx.send("You dont have enough gold i your wallet!")
        return
    
    users[author_name]["wallet"] -= amount
    users[friend_name]["wallet"] += amount

    with open('wallet.json', 'w') as file:
        json.dump(users, file)

    await ctx.send(f'You gifted {amount} gold to {friend_name}.')
################### Economy Commands ####################################

################### Roll mod bot Commands ###############################
@bot.command()
async def rollbot(ctx, bet):
    try:
        bet = int(bet)
    except ValueError:
        await ctx.send('use a number greater than 1')
        return
    
    users = await get_bank_data()
    if str(ctx.author.name) not in users:
        await ctx.send('you dont have a wallet')
        return
    wallet_amt = users[str(ctx.author.name)]["wallet"]
    if wallet_amt < bet:
        await ctx.send('You dont have enough gold')
        return
    
    bot_roll = random.randint(1, bet)
    user_roll = random.randint(1, bet)

    if bot_roll <= user_roll:
        await ctx.send(f'the bot rolled {bot_roll} and you lost {bet} gold')
        users[str(ctx.author.name)]["wallet"] -= bet
    
    else:
        await ctx.send(f'you rolled {user_roll} and won {bet} gold')
        users[str(ctx.author.name)]["wallet"] += bet

    with open('wallet.json', 'w') as file:
        json.dump(users, file)

################### Roll mod bot Commands ###############################

################### Leaderboard Commands ###############################

@bot.command()
async def leaderboard(ctx):
    users = await get_bank_data()

    
    sorted_users = dict(sorted(users.items(), key=lambda x: x[1]["wallet"], reverse=True))
    

    em = discord.Embed(title = f'Leaderboard', color = discord.Color.red())

    for i, (user, data) in enumerate(sorted_users.items()):
        
        em.add_field(name =f'{i+1}. {user}', value=f'{data["wallet"]} gold', inline=False)
    

    await ctx.send(embed = em)
    

################### Leaderboard Commands ###############################

################### Admin Commands ################################

@bot.command()
@commands.has_permissions(administrator=True)
@commands.check(lambda ctx: ctx.author.id in [279627174711918593, 257869280127746050])
async def add_gold(ctx, amount: int, member: discord.Member):
    users = await get_bank_data()

    if amount < 0:
        await ctx.send("du kan ikke sende negativ værdi")
        return
    
    users[str(member.name)]['wallet'] += amount

    with open('wallet.json', 'w') as file:
        json.dump(users, file)

    await ctx.send(f'Gav {amount} gold til {member.name}')

@bot.command()
@commands.has_permissions(administrator=True)
@commands.check(lambda ctx: ctx.author.id in [279627174711918593, 257869280127746050])
async def remove_gold(ctx, amount: int, member: discord.Member):
    users = await get_bank_data()

    if amount < 0:
        await ctx.send("You cannot remove negative amount!")
        return
    
    users[str(member.name)]['wallet'] -= amount

    with open('wallet.json', 'w') as file:
        json.dump(users, file)

    await ctx.send(f'Tog {amount} gold fra {member.name}')

################### Admin Commands ################################



###################  Roll Commands #####################################
@bot.command()
async def funroll(ctx, num):
    try:
        num = int(num)
    except ValueError:
        await ctx.send('Use a number')
        return 
    if num < 2:
        await ctx.send('use a number greater than 1')
        return
    result = random.randint(1, num)
    await ctx.send(f'you rolled {result}!')

###################  Roll Commands #####################################

###################  Beg Commands #####################################

@bot.command()
async def beg(ctx):
    users = await get_bank_data()
    if str(ctx.author.name) not in users:
        await open_account(ctx.author)
        users[str(ctx.author.name)]['last_beg'] = datetime.datetime.now().strftime('%Y-%m-%d')
    
    today = datetime.datetime.now()
    user_date = users[str(ctx.author.name)].get('last_beg')

    if user_date and user_date == today.strftime('%Y-%m-%d'):
        await ctx.send("Stop begging peasant!")

    elif random.random() < 0.5:
        await ctx.send(f"Sorry, I don't give money to peasants or peons.")
        users[str(ctx.author.name)]['last_beg'] = today.strftime('%Y-%m-%d')
        with open('wallet.json', 'w') as file:
            json.dump(users, file)


    else:
        gold_earned = random.randint(100, 500)
        users[str(ctx.author.name)]["wallet"] += gold_earned
        users[str(ctx.author.name)]['last_beg'] = today.strftime('%Y-%m-%d')
        with open('wallet.json', 'w') as file:
            json.dump(users, file)
        await ctx.send(f"You got {gold_earned} gold! Don't come beggin' for more.")

###################  Beg Commands #####################################

###################  Session Commands ##################################

###################  Variabel helvede ###################################

session_active = False
session_users = []
session_cost = 0
prize_pool = {"prize_pool": 0}
game_leader = ""
turn_count = 0
turn_order = ""
game_state = False

###################  Variabel helvede ###################################

@bot.command()
async def session(ctx, cost: int):
    global session_active, session_cost, game_leader, prize_pool

    if session_active:
        await ctx.send('Session already active')
        return
   
    with open ('session.json', 'r') as file:
        game = json.load(file)

    if str(ctx.author.name) in game:
        await ctx.send('Session already active')
    
    game['session_cost'] = cost
    game['prize_pool'] = 0
    prize_pool = {"prize_pool": 0}

    with open('session.json', 'w') as file:
        json.dump(game, file)
    
    users = await get_bank_data()

    if str(ctx.author.name) not in users:
        await open_account(ctx.author)
   
    session_cost = cost
    session_active = True
    

    game_leader = ctx.author
    print(game_leader)

    em = discord.Embed(title = f'Session started, cost is {cost} gold', color = discord.Color.yellow())
    em.add_field(name = 'Started by', value=f'{ctx.author}')
    await ctx.send(embed = em)
    
@bot.command()
async def show_players(ctx):
    global session_users

    player_count = len(session_users)

    if player_count == 0:
        await ctx.send('No player in the session yet!')
        return 

    player_list = "\n".join(session_users)

    em = discord.Embed(title='Session players', color=discord.Color.green())
    em.add_field(name='Amount of players', value=player_count, inline=False)
    em.add_field(name='Players', value=player_list)
    await ctx.send(embed=em)

@bot.command()
async def join(ctx):
    global session_active, session_cost, session_users, prize_pool
    users = await get_bank_data()

    if str(ctx.author.name) not in users:
        await open_account(ctx.author)

    wallet_amt = users[str(ctx.author.name)]["wallet"]

    if game_state:
        await ctx.send("Game already started")
        return

    if not session_active:
        await ctx.send("No session active")
        return

    if str(ctx.author.name) in session_users:
        await ctx.send("You have already joined the session")
        return
    
    if wallet_amt < session_cost:
        await ctx.send("You don't have enough gold to join!")
        return

    users[str(ctx.author.name)]["wallet"] -= session_cost
    
    prize_pool["prize_pool"] += session_cost
    prize_pool["session_cost"] = session_cost
    
    with open('wallet.json', 'w') as file:
        json.dump(users, file)

    with open('session.json', 'w') as file:
        json.dump(prize_pool, file)

    session_users.append(str(ctx.author.name))
    await show_players(ctx)


@bot.command()
async def start(ctx):
    global session_active, game_leader, session_users, prize_pool, turn_count, game_state, session_cost, turn_order

    if (session_active) and (ctx.author == game_leader):
        if turn_count == 0:
            random.shuffle(session_users)
            turn_order = "\n".join([f'{i+1}. {user}' for i, user in enumerate(session_users)])
            em = discord.Embed(title='Game started', color = discord.Color.blue())
            em.add_field(name='Turn order', value= (f'{turn_order}'))
            await ctx.send(embed=em)
            game_state = True
            
        else:
            await ctx.send(f"game already started")        
        turn_count += 1

    else:
        return
    
    turn_count = 0

@bot.command()
async def roll(ctx):
    global session_active, session_users, prize_pool, turn_count, game_state, session_cost, turn_order

    if not session_active or not game_state:
        await ctx.send("The game has not started yet!")
        return
    
    
    if str(ctx.author.name) != str(session_users[turn_count % len(session_users)]):
        await ctx.send("you are not in the game!")
        return
    
    max_roll_value = min(session_cost, prize_pool["session_cost"])
    roll_value = random.randint(1, max_roll_value)

    em = discord.Embed(title='The Roll', color = discord.Color.green())
    em.add_field(name='Player', value= str(ctx.author.name))
    em.add_field(name='Roll:', value= str(roll_value))
    await ctx.send(embed=em)
        

    prize_pool["session_cost"] = roll_value

    with open('session.json', 'w') as file:
        json.dump(prize_pool, file)


    if roll_value == 1:
        print(roll_value)
        users = await get_bank_data()
        user = users[str(ctx.author.name)]
        user["wallet"] += prize_pool["prize_pool"]

            
        with open('wallet.json', 'w') as file:
            json.dump(users, file)

            
        with open('session.json', 'w') as file:
            json.dump(prize_pool, file)

        game_state = False
        session_active = False
        session_users = []
        turn_count = 0
        
        em = discord.Embed(title='Winner', color = discord.Color.gold())
        em.add_field(name='Player', value= str(ctx.author.name))
        em.add_field(name='Prize pool', value= str(prize_pool["prize_pool"]))
        await ctx.send(embed=em)
            
        return
    
    turn_count += 1
    next_player = session_users[turn_count % len(session_users)]
    await ctx.send(f"Next player is {next_player}, and its your turn to roll!")
    return

@bot.command()
@commands.has_permissions(administrator=True)
async def end_session(ctx):
    global session_active, game_state, session_users, turn_count

    if not session_active:
        await ctx.send("No session is active atm!")
        return
    
    session_active = False
    game_state = False
    session_users = []
    turn_count = 0
    await ctx.send('The session has ended. And a new one can be started!')

###################  Session Commands ##################################


###################  Help Commands #####################################


@bot.command()
async def help_command(ctx):
    embed = discord.Embed(title="Command List", description="Here are the available commands:", color=discord.Color.dark_purple())
    
    embed.add_field(name="!balance", value="This is how you open an account or check the amount in your wallet.", inline=False)    
    embed.add_field(name="!rollbot", value="This is a command where you can roll against the bot. Its important to note that you write the amount you want to roll vs the bot e.g: !rollbot 500 ", inline=False)
    embed.add_field(name="!gift", value="This is a command to gift another player. Note that the input should be followed by the amount gifted and which friend to gift. e.g: !gift 500 Nisse", inline=False)
    embed.add_field(name="!leaderboard", value="This command shows the leaderboard and will show all players on the server.", inline=False)
    embed.add_field(name="!funroll", value="This command is just to roll a random number. Its important that you write the number you want to roll between. e.g: !funroll 100.  This will roll a random number between 1-100", inline=False)
    embed.add_field(name="!beg", value="This command will ask the bot for some gold(100-500) win chance is 50/50 and can only be used once a day.", inline=False)
    embed.add_field(name="!help_maingame", value="Writes out the command list for the main game. e.g !help_maingame", inline=False)

    await ctx.send(embed=embed)




@bot.command()
async def help_maingame(ctx):
    embed = discord.Embed(title="Main Game Command List", description="Here are the available commands:", color=discord.Color.dark_purple())
    embed.add_field(name="!session", value="This starts a session where players can join its important that the starter of the session writes the amount of gold that is rolled. e.g: !session 1000", inline=False)    
    embed.add_field(name="!show_players", value="This command shows all players who are currently in the session/game. e.g: !show_players", inline=False)
    embed.add_field(name="!join", value="This command join the session, when !join is written the cost of joining the session is taken from your wallet. e.g: !join", inline=False)
    embed.add_field(name="!start", value="This command starts the session, so when you start the session the bot with select the roll order. When a game is started players cannot join. e.g: !start", inline=False)
    embed.add_field(name="!roll", value="This command rolls, it will always roll from the last rolled number so if last player rolled 100 you will roll from 1-100. e.g: !roll", inline=False)
    
    await ctx.send(embed=embed)


###################  Help Commands #####################################

###################  rules Commands #####################################
@bot.command()
async def gamerules(ctx):

    em = discord.Embed(title='Game Rules', color=discord.Color.dark_purple())
    em.add_field(name="Need help with commands?", value="Use command !help_commands to find the list of commands and how to use them!", inline=False)
    em.add_field(name="Need help with main game commands?", value="Use command !help_maingame to find the list of main game commands and how to use them!", inline=False)
    em.add_field(name="Rollbot", value="The rollbot game is a 50/50 game where you can either double the amount you bet or lose it! To play this game Type !rollbot (amount)", inline=False)
    em.add_field(name="Funroll", value="The fun roll is just a command you can use with friend og for fun to try and roll between 1 and the amount you put! To use this type !funroll (Amount)!", inline=False)
    em.add_field(name="Main Game", value="Need help with the main game? Use command !help. To win the game you need to roll 1 and it is a winner takes all game. The game is started with a session where you can use !join, after some time the game will start or if the session owner use command !start. When the session is stated a roll list will pop up showing who rolls first (useing !roll), and then a message with who is next! Good Luck!!!", inline=False)
    
    await ctx.send(embed=em)

###################  rules Commands #####################################

bot.run(TOKEN)

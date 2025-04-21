import discord
import random
from discord.ext import commands
import sqlite3
import itertools
from discord.ui import Button, View, Select
import re
from PIL import Image
from io import BytesIO
import asyncio
import time

client = commands.Bot(command_prefix='.', intents= discord.Intents.all())
client.remove_command('help')


basecards = ['doge52cb','kermit52st','elonmusk54cb','labran63lb','modi75cam','obama69lm','pepe52cam','huell66cb','kohli61st','rahul67st','rick51rm','noot70gk','steve73rw','teresa67lwb','saul58rb','bateman78lw','chandler79cam','fring60cm','rock77rb','trollface58lb'] 
totwcards = ['speed85lw','masha85cf','skipper83lw','michael88rb','bugsbunny80lb','mario88gk','morbius89rw','tate85cm','spiderman88gk'] 
futurecards = ['bean97gk','kim97cb','ksi96cam','pinkman94lwb','knuckles92cm','yoshi99cb'] 
specialcards = [] 
totycards = ['putin102rw','kratos101cb','elrisitas109st','griffin105cm','shrek106lw'] 
uclcards = []
iconcards = []
totscards = ['gigachad112cam']
alliconcards = []

strikers = ['kohli61st','masha85cf','kermit52st','rahul67st']
goalkeepers = ['noot70gk','bean97gk','mario88gk']
centrebacks = ['doge52cb','elonmusk54cb','huell66cb','kim97cb','kratos101cb']
leftbacks = ['teresa67lwb','bugsbunny80lb','pinkman94lwb','labran63lb']
rightbacks = ['saul58rb','michael88rb']
midfielders = ['modi75cam','obama69lm','pepe52cam','rick51rm','ksi96cam','chandler79cam','tate85cm']
rightwings = ['steve73rw','putin102rw','morbius89rw']
leftwings = ['speed85lw','skipper83lw','obama69lm','rick51rm','bateman78lw','teresa67lwb','pinkman94lwb']


@client.command(aliases=['news'])
async def updates(ctx):
    news1 = "added a new command `.cards` and now you can sell any type of card except ucl"
    
    embed = discord.Embed(title=f"`SONESTAA LEAGUE NEW UPDATES`", description=f"shows you new things the creator added", color=discord.Color.purple())
    embed.add_field(name=f"Recent Updates",value=f"- {news1}")
    
    await ctx.send(embed= embed)
    






@client.event
async def on_ready():
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS real (
        user_id INTEGER, balance INTEGER 
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS toty (
        "user_id", "cards"
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS packs (
        "user_id", "base", "totw", "icons", "futurestars", "toty", "ucl", "special", "tots"
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS team (
        "user_id", "st", "gk", "cb1", "cb2", "lb", "rb", "cm1", "cm2", "cm3", "lw", "rw"
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS best (
        "ovr", "user_id" 
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pmarket (
        "user_id", "s1", "c1", "s2", "c2", "s3", "c3", "s4", "c4", "s5", "c5"
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS events (
        "card", "cardtype", "ovr", "card1", "card2", "card3", "card4", "card5", "coins"
    )''')
    print('bot is ready')

@client.listen()
async def on_message(msg):
    if msg.author.bot:
        return
    author = msg.author
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT user_id FROM real WHERE user_id = {author.id}")
    result = cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO real(user_id, balance) VALUES (?, ?)")
        val = (author.id, 100)
        cursor.execute(sql, val)

    cursor.execute(f"SELECT user_id FROM toty WHERE user_id = {author.id}")
    result = cursor.fetchone()
    if result is None:
        startingcard = ['kermit52st','pepe52cam','doge52cb']
        cursor.execute("INSERT INTO toty(user_id, cards) VALUES (?,?)", (author.id, startingcard[random.randint(0,2)]))

    cursor.execute(f"SELECT user_id FROM packs WHERE user_id = {author.id}")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO packs(user_id, base, totw, icons, futurestars, toty, ucl, special, tots) VALUES (?,?,?,?,?,?,?,?,?)", (author.id, 1, 0, 0, 1, 0, 0, 0, 0))     

    cursor.execute(f"SELECT user_id FROM team WHERE user_id = {author.id}")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO team(user_id, st, gk, cb1, cb2, lb, rb, cm1, cm2, cm3, lw, rw) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    cursor.execute(f"SELECT user_id FROM best WHERE user_id = {author.id}")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO best(ovr, user_id) VALUES (?,?)", (0, author.id))
    
    cursor.execute(f"SELECT user_id FROM pmarket WHERE user_id = {author.id}")
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO pmarket(user_id, s1, c1, s2, c2, s3, c3, s4, c4, s5, c5) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (author.id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
    #Card Summon
    global basecards
    chance = random.randint(1,30)
    card = basecards[random.randint(0,len(basecards) - 1)]
    if chance == 1:
        button = Button(label="PICK", style=discord.ButtonStyle.green, emoji = "✔️")
        async def button_callback(interaction):
            db = sqlite3.connect("real.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM packs WHERE user_id = {interaction.user.id}")
            packs = cursor.fetchone()
            cursor.execute(f"SELECT * FROM toty WHERE user_id = {interaction.user.id}")
            cards = cursor.fetchone()
            if(str(card) in str(cards)):
                await interaction.response.send_message("you already have this card", ephemeral=True)
            else:
                fullcheck = await invfullcheck(interaction.user.id)
                if fullcheck == False:
                    await interaction.response.edit_message(content=f"claimed by <@{interaction.user.id}>",view=None)
                    gcard = ", " + card
                    cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(cards[1]) + gcard, interaction.user.id))
                    db.commit()
                    cursor.close()
                    db.close()
                else:
                    await interaction.response.send_message("Your card inventory is full")
        
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await msg.channel.send(f"{card} just appeared!",file=discord.File(rf'C:\Users\Admin\Desktop\Premier League Bot\cards\{card}.png'),view=view)
    



    db.commit()
    cursor.close()
    db.close()

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Command is still on cooldown, try again in {:.2f}s".format(error.retry_after)
        await ctx.reply(msg)



    
    





#BALANCE    

@client.command(aliases=['bal'])
async def balance(ctx, member:discord.Member = None):
    if member is None:
        member = ctx.author
        
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT balance FROM real WHERE user_id = {member.id}")
    bal = cursor.fetchone()
    try:
        balance = bal[0] 
    except:
        balance = 0

    await ctx.send(f"Your balance is `{balance}`:coin:")

@client.command()
async def team(ctx, user:discord.Member = None):

    card_list = [None, "cards"]

    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    cards = cursor.fetchone()
    cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, cards)]
    cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
    finalcards = cards_[30:]
    upd0 = re.sub('[a-z]', '', finalcards)
    allovr = (re.split(', ',upd0))
    noofcards = len(allovr)
    i = 1
    totalovr = 0
    cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
    allpos = cursor.fetchone()
    cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {ctx.author.id}")
    usermarket = cursor.fetchone()
    
    


    while i != 12:
        player = allpos[i]
        playerovr = re.sub('\D', '', str(player))
        totalovr = int(totalovr) + int(playerovr)
        i = i + 1

    ovr = totalovr/11

    
    if i == 12:

        if allpos[0] == 0 or allpos[1] == 0 or allpos[2] == 0 or allpos[3] == 0 or allpos[4] == 0 or allpos[5] == 0 or allpos[6] == 0 or allpos[7] == 0 or allpos[8] == 0 or allpos[9] == 0 or allpos[10] == 0 or allpos[11] ==0:
            embed = discord.Embed(title=f"`{ctx.author.name}'s TEAM`", description=f"🟥Manager = `{ctx.author}`.          🟦TEAM OVR = you need a filled lineup for an ovr", color=discord.Color.red())
            embed.add_field(name=f"🃏Cards (`{noofcards}`)",value="`"+str(finalcards)+"`")
            embed.add_field(name=f"🧩In Lineup",value=f"`{allpos[1]}\n{allpos[2]}\n{allpos[3]}\n{allpos[4]}\n{allpos[5]}\n{allpos[6]}\n{allpos[7]}\n{allpos[8]}\n{allpos[9]}\n{allpos[10]}\n{allpos[11]}`")
            embed.add_field(name=f":shopping_cart:In Market",value=f"`{usermarket[1]}\n{usermarket[3]}\n{usermarket[5]}\n{usermarket[7]}\n{usermarket[9]}`")
            await ctx.send(embed= embed)
        else:
            
            #lineup filled
            embed = discord.Embed(title=f"`{ctx.author.name}'s TEAM`", description=f"🟥Manager = `{ctx.author}`.          🟦TEAM OVR = __**{round(ovr)}**__,", color=discord.Color.red())
            embed.add_field(name=f"🃏Cards ({noofcards})",value="`"+str(finalcards)+"`")
            embed.add_field(name=f"🧩In Lineup",value=f"`{allpos[1]}\n{allpos[2]}\n{allpos[3]}\n{allpos[4]}\n{allpos[5]}\n{allpos[6]}\n{allpos[7]}\n{allpos[8]}\n{allpos[9]}\n{allpos[10]}\n{allpos[11]}`")
            embed.add_field(name=f":shopping_cart:In Market",value=f"`{usermarket[1]}\n{usermarket[3]}\n{usermarket[5]}\n{usermarket[7]}\n{usermarket[9]}`")
            await ctx.send(embed= embed)
            cursor.execute(f"SELECT * FROM best WHERE user_id = {ctx.author.id}")
            cursor.execute("UPDATE best SET ovr = ? WHERE user_id = ?", (round(int(ovr)), ctx.author.id))
            db.commit()
    
@client.command()
async def cards(ctx):
    card_list = [None, "cards"]

    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    cards = cursor.fetchone()
    cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, cards)]
    cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
    finalcards = cards_[30:]
    fcl = finalcards.split(', ')
    noofcards = len(fcl)
    i = 0
    BC = ""
    TOW = ""
    ICON = ""
    FS = ""
    TOY = ""
    TOS = ""
    SP = ""
    UCL = ""
    while i != noofcards:
        if(fcl[i] in basecards):
            BC = BC + str(fcl[i]) + ", "
        if(fcl[i] in totwcards):
            TOW = TOW + str(fcl[i]) + ", "
        if(fcl[i] in alliconcards):
            ICON = ICON + str(fcl[i]) + ", "
        if(fcl[i] in futurecards):
            FS = FS + str(fcl[i]) + ", "
        if(fcl[i] in totycards):
            TOY = TOY + str(fcl[i]) + ", "
        if(fcl[i] in totscards):
            TOS = TOS + str(fcl[i]) + ", "
        if(fcl[i] in specialcards):
            SP = SP + str(fcl[i]) + ", "
        if(fcl[i] in uclcards):
            UCL = UCL + str(fcl[i]) + ", "
        i = i + 1
        
    embed = discord.Embed(title=f"`🃏Your Cards🃏`", description=f"These are your cards sorted by pack type", color=discord.Color.dark_red())
    if str(BC) != "":
        embed.add_field(name=f"**Base**",value=f"`{BC}`",inline=False)
    if str(TOW) != "":
        embed.add_field(name=f"**Totw**",value=f"`{TOW}`",inline=False)
    if str(FS) != "":
        embed.add_field(name=f"**Futurestars**",value=f"`{FS}`",inline=False)
    if str(TOY) != "":
        embed.add_field(name=f"**Toty**",value=f"`{TOY}`",inline=False)
    if str(ICON) != "":
        embed.add_field(name=f"**Icon**",value=f"`{ICON}`",inline=False)
    if str(UCL) != "":
        embed.add_field(name=f"**Ucl**",value=f"`{UCL}`",inline=False)
    if str(TOS) != "":
        embed.add_field(name=f"**Tots**",value=f"`{TOS}`",inline=False)
    if str(SP) != "":
        embed.add_field(name=f"**Special**",value=f"`{SP}`",inline=False)
    
    
    await ctx.send(embed= embed)

    
@client.command()
async def packs(ctx):
    packlist = [None, "`Base`", "`Totw`", "`Icons`", "`Futurestars`", "`Toty`", "`Ucl`", "`Special`", "`Tots`"]

    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM packs WHERE user_id = {ctx.author.id}")
    packs = cursor.fetchone()
    packs_ = [f"{i} x{j}" for i, j in itertools.zip_longest(packlist, packs) if int(j) > 0 and int(j) < 10000000000000] 
    packs_ = "\n".join(packs_) if int(len(packs_)) > 0 else "*You dont have any packs*"
    _packs = packs_.lower()
    embed = discord.Embed(title="`Packs Inventory`", description="All your packs.\n To open a pack do .open [PACK_NAME]\n\n for example- `.open base`.", color=discord.Color.blue())
    embed.add_field(name="Packs",value=_packs)
    await ctx.send(embed= embed)

@client.command()
async def show(ctx, card = None):
    card_list = [None, "cards"]

    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    cards = cursor.fetchone()
    cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, cards)]
    cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
    finalcards = cards_[30:]
    fcl = finalcards.split(', ')
    fcl.sort()
    
    i = 0

    if card == None:
        olist = []
        olist2 = []
        while i != len(fcl): #len(fcl) is no of cards
            optioncard = fcl[i]
            if len(olist) == 25:
                if(str(optioncard) in basecards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="🟫"))
                if(str(optioncard) in totwcards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="🟧"))
                if(str(optioncard) in futurecards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="🟪"))
                if(str(optioncard) in totycards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="🟦"))
                if(str(optioncard) in alliconcards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="🟨"))
                if(str(optioncard) in uclcards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="🟩"))
                if(str(optioncard) in totscards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="⬛"))
                if(str(optioncard) in specialcards):
                    olist2.append(discord.SelectOption(label=optioncard,emoji="⏹"))
                
                i = i + 1
            else:
                
                if(str(optioncard) in basecards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟫"))
                if(str(optioncard) in totwcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟧"))
                if(str(optioncard) in futurecards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟪"))
                if(str(optioncard) in totycards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟦"))
                if(str(optioncard) in alliconcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟨"))
                if(str(optioncard) in uclcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟩"))
                if(str(optioncard) in totscards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="⬛"))
                if(str(optioncard) in specialcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="⏹"))               
                
                i = i + 1
        if len(olist) == 0:
            select = Select(placeholder="You do not have any cards",options=[
                discord.SelectOption(label="0")
            ])
            select2 = Select(placeholder="You do not have any cards",options=[
                discord.SelectOption(label="0")
            ])
        else:
            if len(olist2) > 0:
                select = Select(placeholder="List 1",options=olist)
                select2 = Select(placeholder="List 2",options=olist2)
            else:
                select = Select(placeholder="List 1",options=olist)
                select2 = Select(options=[discord.SelectOption(label="0")])
                    
        async def my_callback(interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.response.edit_message(content=f"`{select.values[0]}`", view=None)
                await ctx.reply(f"`{ctx.author}'s card`",file=discord.File(rf'C:\Users\Admin\Desktop\Premier League Bot\cards\{select.values[0]}.png'))
            else:
                await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
        async def my_callback2(interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.response.edit_message(content=f"`{select2.values[0]}`", view=None)
                await ctx.reply(f"`{ctx.author}'s card`",file=discord.File(rf'C:\Users\Admin\Desktop\Premier League Bot\cards\{select2.values[0]}.png'))
            else:
                await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
        select.callback = my_callback
        select2.callback = my_callback2
        view = View()
        view.add_item(select)
        if len(olist2) > 0:
            view.add_item(select2)
        if i == len(fcl):
            await ctx.reply("Select Your Card",view=view)
    else:
        if(str(card) in finalcards):
            await ctx.send(f"`{ctx.author}'s card`" ,file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
        else:
            await ctx.reply("You dont have that card!")






########################################################How to
@client.command()
async def howto(ctx):
   
    embed = discord.Embed(title="**`❔HOW TO PLAY❔`**", description="the bot prefix is .", color=discord.Color.blue())
    embed.add_field(name="**💰Economy💰**",value="`.merch` - gives you money for selling team merch\n`.bet` - earns or loses money of max 100\n`.lottery` - earns random amount of money (bonus chance for packs)\n`.balance` - shows your current balance\n`.sex` - seggs money\n`.shop` - shows items you can buy\n`.buy [ITEM_NAME]` - used to buy items such as packs\n`.sell [CARD]` - sells a card for its pack type price\n`.wheel` - spin a wheel for prices")
    embed.add_field(name="**📦Packs📦**",value="`.open [PACK_NAME]` - opens a pack\n`.trade @User [GIVING_CARD] [RECEIVING_CARD]` - used to trade two cards between two players\n`.exchanges` - used to see current exchanges\n`.exc [PACK] [CARD1] [CARD2] [CARD3]` - used to exchange cards for packs\n`.give [CARD] [PLAYER]` - donate a card to a player\n`.show [CARD]` - shows the card picture if you own it")
    embed.add_field(name="**⚽Team⚽**",value="`.team` - shows your cards, positions and ovr\n`.positions` - used to see your current player positions\n`.lineup` - used to view your team lineup\n`.set [CARD] [POS]` - set a card in a certain position\n`.remove [POS]` - remove a card from a certain position\n`.leaderboard` - shows the leaderboard based on OVR")
    embed.add_field(name="**🎮Play🎮**",value="`.match [BET] [PLAYER2]` - Play a match between 2 players")
    embed.add_field(name="**🎈Events🎈**",value="`.events [EVENT NUMBER]` - view ongoing events\n`.redeem [EVENT NUMBER]` - redeem prizes for ongoing events")
    await ctx.send(embed= embed)
######################################################################################################




    





#PACK OPENING
##
##
##
##

@client.command()
@commands.cooldown(1,10,commands.BucketType.user)
async def open(ctx, pack):
    fullcheck = await invfullcheck(ctx.author.id)
    if fullcheck == False:
        global basecards
        global futurecards
        global totwcards
        global totycards
        global specialcards
        global iconcards
        if pack == 'base':
            packno = 1
            cardlib = basecards
        if pack == 'totw':
            packno = 2
            cardlib = totwcards
        if pack == 'icon':
            packno = 3
            cardlib = alliconcards
        if pack == 'futurestars':
            packno = 4
            cardlib = futurecards
        if pack == 'toty':
            packno = 5
            cardlib = totycards
        if pack == 'ucl':
            packno = 6
            cardlib = uclcards
        if pack == 'special':
            packno = 7
            cardlib = specialcards
        if pack == 'tots':
            packno = 8
            cardlib = totscards
        
        db = sqlite3.connect("real.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM packs WHERE user_id = {ctx.author.id}")
        packs = cursor.fetchone()
        cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
        cards = cursor.fetchone()
        if int(packs[packno]) > 0:            
            cursor.execute("UPDATE packs SET base = ? WHERE user_id = ?", (int(packs[packno]) - 1, ctx.author.id))
            db.commit()
            await ctx.reply(f"opening {pack} pack...")
            n = random.randint(0,len(cardlib) - 1)
            card = cardlib[n]
            await ctx.send(f"{ctx.author} has opened this card", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
            gcard = f", {card}"
            if(str(card) in str(cards)):
                await ctx.reply("You already have this card, therefore it is being removed L, you get another pack tho")
                cursor.execute(f"UPDATE packs SET {pack} = ? WHERE user_id = ?", (int(packs[packno]), ctx.author.id))
                db.commit()
                cursor.close()
                db.close()
            else:   
                
                cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(cards[1]) + gcard, ctx.author.id))
                db.commit()
                cursor.close()
                db.close()
                await ctx.reply("`card added to inventory`")
        else:
            await ctx.reply(f"You dont have any {pack} card packs!")
            cursor.close()
            db.close()
    else:
        await ctx.reply("Your card inventory is full.")
    


        
@client.command()
async def trade(ctx, user: discord.Member, send, receive):
    if ctx.author.id != user.id:
        button = Button(label="Confirm Trade", style=discord.ButtonStyle.blurple)
        button2 = Button(label="Decline Trade", style=discord.ButtonStyle.red)
        async def button_callback(interaction):
            if interaction.user.id == user.id:
                db = sqlite3.connect("real.sqlite")
                cursor = db.cursor()
                cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(scards).replace(send, receive), ctx.author.id))
                cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(rcards).replace(receive, send), user.id))
                db.commit()
                await interaction.response.edit_message(content="trade accepted!", view=None)
                cursor.close()
                db.close()
            else:
                await interaction.response.send_message("this is not for you", ephemeral=True)
                
        async def button2_callback(interaction):
            if interaction.user.id == user.id:
                db = sqlite3.connect("real.sqlite")
                cursor = db.cursor()
                await interaction.response.edit_message(content="trade declined!", view=None)
                await interaction.followup.send(f"<@{ctx.author.id}>, <@{user.id}> has declined your trade offer")
                cursor.close()
                db.close()
        button.callback = button_callback
        button2.callback = button2_callback
        view = View()
        view.add_item(button)
        view.add_item(button2)
        if isinstance(send, str) and isinstance(receive, str):
            db = sqlite3.connect("real.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
            ownedcards1 = cursor.fetchone()
            scards = ownedcards1[1]
  
            cursor.execute(f"SELECT * FROM toty WHERE user_id = {user.id}")
            ownedcards2 = cursor.fetchone()
            rcards = ownedcards2[1]


            if(str(send) in str(scards)) and (str(receive) in str(rcards)):
                if(str(send) in str(rcards)) and (str(receive) in str(scards)):
                    
                    await ctx.reply("the receiver already has this card, or you already have the card you're asking")
                else:
                    check1 = await lineupcheck(send, ctx.author.id)
                    check2 = await lineupcheck(receive, user.id)
                    if check1 == False and check2 == False:
                        await ctx.reply(f"<@{user.id}>, do you want to accept this trade with {ctx.author}\n\n <@{ctx.author.id}> wants `{receive}` for `{send}`", view=view)
                    else:
                        await ctx.reply("One of those cards are in a lineup, remove them from a lineup to be able to be traded")
                    
            else:
                await ctx.reply("invalid cards")
        else:
            await ctx.reply("You can only trade cards for cards")
    else:
        await ctx.reply("bro really tried to find a loophole, you cant trade with yourself lonelyass")


#ADMIN ONLY COMMANDS
@client.command()
async def drop(ctx):
    if ctx.author.id == 583246523664433162:
        button = Button(label="CLAIM", style=discord.ButtonStyle.green, emoji = "✔️")
        async def button_callback(interaction):
            db = sqlite3.connect("real.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM packs WHERE user_id = {interaction.user.id}")
            packs = cursor.fetchone()
            print(packs)
            cursor.execute("UPDATE packs SET special = ? WHERE user_id = ?", (int(packs[7]) + 1, interaction.user.id))
            db.commit()
            await interaction.response.edit_message(content=f"claimed by <@{interaction.user.id}>",view=None)
            cursor.close()
            db.close()
        button.callback = button_callback
        view = View()
        view.add_item(button)
        await ctx.send("**MILAN HAS DROPPED SPECIAL PACK, CLICK THE BUTTON TO CLAIM IT**", view=view)

    else:
        await ctx.reply("Only milan can use this command loude")

@client.command()
async def add(ctx, card):
    if ctx.author.id == 583246523664433162:
        card_list = [None, "cards"]

        db = sqlite3.connect("real.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
        cards = cursor.fetchone()
        cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, cards)]
        cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
        finalcards = cards_[30:]
        addedcard = ", " + card

        cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (finalcards + addedcard, ctx.author.id))
        await ctx.reply(f"added `{card}` to your inventory!")
        db.commit()
        cursor.close()
        db.close()
    else:
        await ctx.reply("Only milan (the great) can use this command")

    
#economy mark

@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def bet(ctx):
    earnings = random.randint(-100, 100)
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT balance FROM real WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()

    cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (wallet[0] + int(earnings), ctx.author.id))
    await ctx.reply(f"betting on matches gave you `{earnings}`:coin:")

    db.commit()
    cursor.close()
    db.close()














#shoppp
@client.command()
async def shop(ctx):
    embed = discord.Embed(title="**`Shop`**", description="Shop Items.\n To buy an item do `.buy [ITEM]`\n\n for example- `.buy base`.", color=discord.Color.green())
    embed.add_field(name="**Packs**",value="base - `500`:coin:\nicon - `20,000`:coin:")
    await ctx.send(embed= embed)

@client.command()
async def buy(ctx, item):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()

    cursor.execute(f"SELECT balance FROM real WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()
    cursor.execute(f"SELECT * FROM packs WHERE user_id = {ctx.author.id}")
    packs = cursor.fetchone()
    if item == "base":
        if wallet[0] >= 500:
            cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (wallet[0] - 500, ctx.author.id))
            cursor.execute(f"UPDATE packs SET base = ? WHERE user_id = ?", (int(packs[1]) + 1, ctx.author.id))
            await ctx.reply(f"You have bought `1 base pack` for 500:coin:, current balance is `{wallet[0] - 500}`:coin:")
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.reply(f"You dont have enough coins for that. you have {wallet[0]}:coin:")
            cursor.close()
            db.close()
    if item == "icon":
        if wallet[0] >= 20000:
            cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (wallet[0] - 20000, ctx.author.id))
            cursor.execute(f"UPDATE packs SET icons = ? WHERE user_id = ?", (int(packs[3]) + 1, ctx.author.id))
            await ctx.reply(f"You have bought `1 icon pack` for 20000:coin:, current balance is `{wallet[0] - 20000}`:coin:")
            db.commit()
            cursor.close()
            db.close()
        else:
            await ctx.reply(f"You dont have enough coins for that. you have {wallet[0]}:coin:")
            cursor.close()
            db.close()
    
    
   




#cardexchanges
@client.command()
async def exchanges(ctx):
    embed = discord.Embed(title="**`Exchanges`**", description="Exchange cards for packs.\n To exchange cards do `.exc [PACK TYPE]`, example- `.exc totw`.", color=discord.Color.yellow())
    embed.add_field(name="**Current Exchanges**",value="`totw pack` - 3 base cards\n`futurestars pack` - 3 totw cards\n`toty pack` - 3 futurestars cards\n")
    await ctx.send(embed= embed)

@client.command()
@commands.cooldown(1,5,commands.BucketType.user)
async def exc(ctx, pack, c1=None, c2=None, c3=None):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    cards = cursor.fetchone()
    cursor.execute(f"SELECT * FROM packs WHERE user_id = {ctx.author.id}")
    packs = cursor.fetchone()
    global basecards
    global totwcards
    global futurecards
    card_list = [None, "cards"]

    cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, cards)]
    cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
    finalcards = cards_[30:]
    fcl = finalcards.split(', ')
    i = 0
    if c1 == None:
        if len(fcl)<3:
            await ctx.reply("you dont even have 3 cards in total")
        else:
            olist = []
            while i != len(fcl): #len(fcl) is no of cards
                optioncard = fcl[i]
                if pack == "totw":
                    cardno = 2
                    select = Select(max_values=3,min_values=3,placeholder="3 base card players🟫",options=olist)
                    if(str(optioncard) in basecards):
                        lc = await lineupcheck(optioncard, ctx.author.id)
                        if lc == False:
                            olist.append(discord.SelectOption(label=optioncard,emoji="🟫"))
                if pack == "futurestars":
                    cardno = 4
                    select = Select(max_values=3,min_values=3,placeholder="3 totw card players🟧",options=olist)
                    if(str(optioncard) in totwcards):
                        lc = await lineupcheck(optioncard, ctx.author.id)
                        if lc == False:
                            olist.append(discord.SelectOption(label=optioncard,emoji="🟧"))
                if pack == "toty":
                    cardno = 5
                    select = Select(max_values=3,min_values=3,placeholder="3 futurestars card players🟪",options=olist)
                    if(str(optioncard) in futurecards):
                        lc = await lineupcheck(optioncard, ctx.author.id)
                        if lc == False:
                            olist.append(discord.SelectOption(label=optioncard,emoji="🟪"))
                i = i + 1
                

            async def my_callback(interaction):
                if interaction.user.id == ctx.author.id:
                    await interaction.response.edit_message(content=f"`{select.values[0]}`,`{select.values[1]}`,`{select.values[2]}`",view=None)
                    c1 = select.values[0]
                    c2 = select.values[1]
                    c3 = select.values[2]

                    await ctx.reply(f"exchanged `{c1}`,`{c2}`,`{c3}` for a `{pack} pack`!")
                    _c1 = f"{c1}, "
                    _c2 = f"{c2}, "
                    _c3 = f"{c3}, "
                    upd0 = str(cards[1]) + ", "
                    upd1 = str(upd0).replace(_c1, "")
                    upd2 = str(upd1).replace(_c2, "")
                    upd3 = str(upd2).replace(_c3, "")
                    upd4 = str(upd3[:-2])                       #removes last 2 comma and space

                    cursor.execute(f"UPDATE packs SET {pack} = ? WHERE user_id = ?", (int(packs[cardno]) + 1, ctx.author.id))
                    cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd4), ctx.author.id))
                    db.commit()
                else:
                    await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
                #end
            select.callback = my_callback
            view = View()
            view.add_item(select)
            if i == len(fcl):
                if len(olist)<3:
                    await ctx.reply("you dont have the required amount of cards for exchange (try removing cards from lineup)")
                else:
                    await ctx.reply(f"Select 3 Cards to exchange for a {pack} pack",view=view)
    else:
    
        if pack == "totw":
            if(str(c1) in cards[1]) and (str(c2) in cards[1]) and (str(c3) in cards[1]):
                check1 = await lineupcheck(c1, ctx.author.id)
                check2 = await lineupcheck(c2, ctx.author.id)
                check3 = await lineupcheck(c3, ctx.author.id)
                if check1 == False and check2 == False and check3 == False:
                    if(str(c1) in basecards) and (str(c2) in basecards) and (str(c3) in basecards):
                        if c1 != c2 != c3:
                            await ctx.reply(f"exchanged `{c1}`,`{c2}`,`{c3}` for a `totw pack`!")
                            _c1 = f"{c1}, "
                            _c2 = f"{c2}, "
                            _c3 = f"{c3}, "
                            upd0 = str(cards[1]) + ", "
                            upd1 = str(upd0).replace(_c1, "")
                            upd2 = str(upd1).replace(_c2, "")
                            upd3 = str(upd2).replace(_c3, "")
                            upd4 = str(upd3[:-2])                       #removes last 2 comma and space

                            cursor.execute(f"UPDATE packs SET totw = ? WHERE user_id = ?", (int(packs[2]) + 1, ctx.author.id))
                            cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd4), ctx.author.id))
                            db.commit()
                        else:
                            await ctx.reply("you wrote the same card twice (advaith i fixed that loophole L)")
                    else:
                        await ctx.reply("the given cards are not base cards.")
                else:
                    await ctx.reply("One or more of those cards are in a lineup, remove them from a lineup in order to be exchanged")
                
            else:
                await ctx.reply("invalid cards.")
        if pack == "futurestars":
            if(str(c1) and str(c2) and str(c3) in cards[1]):
                check1 = await lineupcheck(c1, ctx.author.id)
                check2 = await lineupcheck(c2, ctx.author.id)
                check3 = await lineupcheck(c3, ctx.author.id)
                if check1 == False and check2 == False and check3 == False:
                    if(str(c1) and str(c2) and str(c3) in totwcards):
                        if c1 != c2 != c3:
                            await ctx.reply(f"exchanged `{c1}`,`{c2}`,`{c3}` for a `futurestars pack`!")
                            _c1 = f"{c1}, "
                            _c2 = f"{c2}, "
                            _c3 = f"{c3}, "
                            upd0 = str(cards[1]) + ", "
                            upd1 = str(upd0).replace(_c1, "")
                            upd2 = str(upd1).replace(_c2, "")
                            upd3 = str(upd2).replace(_c3, "")
                            upd4 = str(upd3[:-2])                       #removes last 2 comma and space

                            cursor.execute(f"UPDATE packs SET futurestars = ? WHERE user_id = ?", (int(packs[4]) + 1, ctx.author.id))
                            cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd4), ctx.author.id))
                            db.commit()
                        else:
                            await ctx.reply("you wrote the same card twice (advaith i fixed that loophole L)")
                    else:
                        await ctx.reply("the given cards are not totw cards.")
                else:
                    await ctx.reply("One or more of those cards are in a lineup, remove them from a lineup in order to be exchanged")
                
                
            else:
                await ctx.reply("invalid cards.")
        if pack == "toty":
            if(str(c1) and str(c2) and str(c3) in cards[1]):
                check1 = await lineupcheck(c1, ctx.author.id)
                check2 = await lineupcheck(c2, ctx.author.id)
                check3 = await lineupcheck(c3, ctx.author.id)
                if check1 == False and check2 == False and check3 == False:
                    if(str(c1) and str(c2) and str(c3) in futurecards):
                        if c1 != c2 != c3:
                            await ctx.reply(f"exchanged `{c1}`,`{c2}`,`{c3}` for a `toty pack`!")
                            _c1 = f"{c1}, "
                            _c2 = f"{c2}, "
                            _c3 = f"{c3}, "
                            upd0 = str(cards[1]) + ", "
                            upd1 = str(upd0).replace(_c1, "")
                            upd2 = str(upd1).replace(_c2, "")
                            upd3 = str(upd2).replace(_c3, "")
                            upd4 = str(upd3[:-2])                       #removes last 2 comma and space

                            cursor.execute(f"UPDATE packs SET toty = ? WHERE user_id = ?", (int(packs[5]) + 1, ctx.author.id))
                            cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd4), ctx.author.id))
                            db.commit()
                        else:
                            await ctx.reply("you wrote the same card twice (advaith i fixed that loophole L)")
                    else:
                        await ctx.reply("the given cards are not futurestars cards.")
                else:
                    await ctx.reply("One or more of those cards are in a lineup, remove them from a lineup in order to be exchanged")
                
                
            else:
                await ctx.reply("invalid cards.")
        if pack == "tots":
            if(str(c1) and str(c2) and str(c3) in cards[1]):
                check1 = await lineupcheck(c1, ctx.author.id)
                check2 = await lineupcheck(c2, ctx.author.id)
                check3 = await lineupcheck(c3, ctx.author.id)
                if check1 == False and check2 == False and check3 == False:
                    if(str(c1) and str(c2) and str(c3) in alliconcards):
                        if c1 != c2 != c3:
                            await ctx.reply(f"exchanged `{c1}`,`{c2}`,`{c3}` for a `tots pack`!")
                            _c1 = f"{c1}, "
                            _c2 = f"{c2}, "
                            _c3 = f"{c3}, "
                            upd0 = str(cards[1]) + ", "
                            upd1 = str(upd0).replace(_c1, "")
                            upd2 = str(upd1).replace(_c2, "")
                            upd3 = str(upd2).replace(_c3, "")
                            upd4 = str(upd3[:-2])                       #removes last 2 comma and space

                            cursor.execute(f"UPDATE packs SET tots = ? WHERE user_id = ?", (int(packs[8]) + 1, ctx.author.id))
                            cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd4), ctx.author.id))
                            db.commit()
                        else:
                            await ctx.reply("you wrote the same card twice (advaith i fixed that loophole L)")
                    else:
                        await ctx.reply("the given cards are not icon cards.")
                else:
                    await ctx.reply("One or more of those cards are in a lineup, remove them from a lineup in order to be exchanged")
                
                
            else:
                await ctx.reply("invalid cards.")
 




















############### FUNCTIONS

async def lineupcheck(card, user): #checks if card is in a lineup
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {user}")
    allpos = cursor.fetchone()
    if(str(card) in str(allpos)):
        return True
    else:
        return False

async def ownershipcheck(card, user): #checks if user owns card
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {user}")
    ownedcards = cursor.fetchone()
    allcards = ownedcards[1]
    everycard = (re.split(', ',allcards))
    if(str(card) in str(everycard)):
        return True
    else:
        return False

async def invfullcheck(user):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {user}")
    ownedcards = cursor.fetchone()
    allcards = ownedcards[1]
    everycard = (re.split(', ',allcards))
    if len(everycard) == 50:
        return True
    else:
        return False





#TEAM SETTINGS 

@client.command(aliases=['pos'])
async def positions(ctx):

    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
    allpos = cursor.fetchone()

    #checkinteam

    



    
    
    embed = discord.Embed(title="`Player Positions`", description=f"do assign players to different positions, do `.set [position] [card]`", color=discord.Color.light_gray())
    embed.add_field(name=f"Current Positions",value=f"**Goalkeeper** `gk` = {allpos[2]}\n**Left Back** `lb` = {allpos[5]}\n**Right Back** `rb` = {allpos[6]}\n**Centre Back 1** `cb1` = {allpos[3]}\n**Centre Back 2** `cb2` = {allpos[4]}\n**Midfielder Left** `cm1` = {allpos[7]}\n**Midfielder Centre** `cm2` = {allpos[8]}\n**Midfielder Right** `cm3` = {allpos[9]}\n**Striker** `st` = {allpos[1]}\n**Left Wing** `lw` = {allpos[10]}\n**Right Wing** `rw` = {allpos[11]}")
    await ctx.send(embed= embed)
    



@client.command()
async def set(ctx, p, card):

    global strikers
    global goalkeepers
    global centrebacks
    global leftbacks
    global rightbacks
    global midfielders
    global leftwings
    global rightwings


    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
    allpos = cursor.fetchone()
    card_list = [None, "cards"]
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    ownedcards = cursor.fetchone()
    cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, ownedcards)]
    cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
    finalcards = cards_[30:]
    fcl = finalcards.split(', ')
    i = 0

    if p == "st":
        cursor.execute(f"SELECT st FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in strikers):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your striker position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET st = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a striker, you can only put cards with an `ST` in their position here. centre forwards `CF` can also be put here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "gk":
        cursor.execute(f"SELECT gk FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in goalkeepers):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your goalkeeper position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET gk = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a goalkeeper, you can only put cards with an `GK` in their position here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "cb1":
        cursor.execute(f"SELECT cb1 FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in centrebacks):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your centre back position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET cb1 = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a centre back, you can only put cards with an `CB` in their position here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "cb2":
        cursor.execute(f"SELECT cb2 FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in centrebacks):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your centre back position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET cb2 = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a centre back, you can only put cards with an `CB` in their position here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "rb":
        cursor.execute(f"SELECT rb FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in rightbacks):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your right back position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET rb = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a right back, you can only put cards with an `RB` in their position here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "lb":
        cursor.execute(f"SELECT lb FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in leftbacks):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your left back position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET lb = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a left back, you can only put cards with an `LB` in their position here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "cm1":
        cursor.execute(f"SELECT cm1 FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in midfielders):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your midfielder position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET cm1 = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a midfielder, you can only put cards with an `CM` in their position here, centre attacking `CAM` and defending midfielders `CDM` can also be put here, along with left mids `LM` and right mids `RM`")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "cm2":
        cursor.execute(f"SELECT cm2 FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in midfielders):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your midfielder position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET cm2 = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a midfielder, you can only put cards with an `CM` in their position here, centre attacking `CAM` and defending midfielders `CDM` can also be put here, along with left mids `LM` and right mids `RM`")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "cm3":
        cursor.execute(f"SELECT cm3 FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in midfielders):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your midfielder position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET cm3 = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a midfielder, you can only put cards with an `CM` in their position here, centre attacking `CAM` and defending midfielders `CDM` can also be put here, along with left mids `LM` and right mids `RM`")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "rw":
        cursor.execute(f"SELECT rw FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in rightwings):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your right winger position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET rw = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a right winger, you can only put cards with an `RW` in their position here, Right Mids 'RM' and Right Wing Backs `RWB` can also be placed here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()
    if p == "lw":
        cursor.execute(f"SELECT lw FROM team WHERE user_id = {ctx.author.id}")
        prevc = cursor.fetchone()
        if(str(card) in ownedcards[1]):
            if(str(card) in leftwings):
                if(str(card) in allpos):
                    await ctx.reply("That card is already placed in this team")
                    cursor.close()
                    db.close()
                else:
                    await ctx.reply(f"you have set `{card}` in your left winger position, removing {prevc}", file=discord.File(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{card}.png'))
                    cursor.execute(f"UPDATE team SET lw = ? WHERE user_id = ?", (card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()

            else:
                await ctx.reply("That card is not a left winger, you can only put cards with an `LW` in their position here, Left Mids 'LM' and Left Wing Backs `LWB` can also be placed here")
                cursor.close()
                db.close()
        else:
            await ctx.reply("You do not own this card.")
            cursor.close()
            db.close()

@client.command()
async def remove(ctx, pos):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
    allpos = cursor.fetchone()
    
    cursor.execute(f"UPDATE team SET {str(pos)} = ? WHERE user_id = ?", (0, ctx.author.id))
    db.commit()

    await ctx.reply(f"you have removed your `{pos}`  from lineup")





@client.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def lineup(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {user.id}")
    allpos = cursor.fetchone()
    



    if allpos[0] == 0 or allpos[1] == 0 or allpos[2] == 0 or allpos[3] == 0 or allpos[4] == 0 or allpos[5] == 0 or allpos[6] == 0 or allpos[7] == 0 or allpos[8] == 0 or allpos[9] == 0 or allpos[10] == 0 or allpos[11] ==0:
        await ctx.reply(f"{user}'s is not filled. do `.set` to set your players")
    else:
    
        field = Image.open("lineup.png")
        
        st = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[1]}.png')
        st = st.resize((170,220))
        gk = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[2]}.png')
        gk = gk.resize((170,220))
        cb1 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[3]}.png')
        cb1 = cb1.resize((170,220))
        cb2 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[4]}.png')
        cb2 = cb2.resize((170,220))
        lb = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[5]}.png')
        lb = lb.resize((170,220))
        rb = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[6]}.png')
        rb = rb.resize((170,220))
        cm1 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[7]}.png')
        cm1 = cm1.resize((170,220))
        cm2 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[8]}.png')
        cm2 = cm2.resize((170,220))
        cm3 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[9]}.png')
        cm3 = cm3.resize((170,220))
        lw = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[10]}.png')
        lw = lw.resize((170,220))
        rw = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{allpos[11]}.png')
        rw = rw.resize((170,220))
        

        field.paste(gk, (515,450), gk)
        field.paste(cb1, (315,350), cb1)
        field.paste(cb2, (715,350), cb2)
        field.paste(cm2, (515,200), cm2)
        field.paste(cm1, (130,200), cm1)
        field.paste(cm3, (900,200), cm3)
        field.paste(st, (515,0), st)
        field.paste(lw, (130,0), lw)
        field.paste(rw, (900,0), rw)  
        field.paste(lb, (30,400), lb)
        field.paste(rb, (1000,400), rb)  
        


        field.save("lineup-update.png")
        
        await ctx.send(f"<@{user.id}>'s team",file= discord.File("lineup-update.png"))
    









    

 




#EVENTS MARK
@client.command()
async def eventmaker(ctx, card, cardtype, ovr, exc1, exc2, exc3, exc4, exc5, price):
    if ctx.author.id == 583246523664433162:
        db = sqlite3.connect("real.sqlite")
        cursor = db.cursor()
        cursor.execute("INSERT INTO events(card, cardtype, ovr, card1, card2, card3, card4, card5, coins) VALUES (?,?,?,?,?,?,?,?,?)", (card, cardtype, ovr, exc1, exc2, exc3, exc4, exc5, price))
        db.commit()
        await ctx.reply("new event added")
    else:
        await ctx.reply("only qmilano can use this command")




@client.command()
async def events(ctx, event = None):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute("SELECT * from events")
    eventslist = cursor.fetchall()
    i = 0
    eventcards = []
    if event == None:
        while i != len(eventslist):
            currentevent = eventslist[i]
            currenteventcard = currentevent[0]
            eventcards.append(str(currenteventcard))
            i = i + 1
        if i == len(eventslist):
            u0 = str(eventcards)
            u1 = u0.replace("[","")
            u2 = u1.replace("]","")
            u3 = u2.replace("',","\n")
            u4 = u3.replace("'","1. ")
            await ctx.reply(u4) 
    
@client.command()
async def redeem(ctx, event):
    fullcheck = await invfullcheck(ctx.author.id)
    if fullcheck == False:
        db = sqlite3.connect("real.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
        ownedcards = cursor.fetchone()
        allcards = ownedcards[1]
        everycard = (re.split(', ',allcards))
        cursor.execute(f"SELECT balance FROM real WHERE user_id = {ctx.author.id}")
        wallet = cursor.fetchone()
        if event == "1":
            if("mrvundela107rb" in ownedcards):
                await ctx.reply("You already have the event card")
            else:
                if("mithun101rb" in str(everycard)) and ("rohit81st" in str(everycard)) and ("sonu99st" in str(everycard)) and (int(wallet[0]) >= 1000):
                    check1 = await lineupcheck("mithun101rb", ctx.author.id)
                    check2 = await lineupcheck("rohit81st", ctx.author.id)
                    check3 = await lineupcheck("sonu99st", ctx.author.id)
                    if check1 == False and check2 == False and check3 == False:
                
                        cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (wallet[0] - 1000, ctx.author.id))
                        db.commit()
                        
                        upd0 = str(ownedcards[1]) + ", "
                        
                        upd1 = str(upd0).replace("mithun101rb, ", "")
                        upd2 = str(upd1).replace("rohit81st, ", "")
                        upd3 = str(upd2).replace("sonu99st, ", "")
                        upd4 = str(upd3[:-2])
                        upd5 = str(upd4) + ", mrvundela107rb"
                        print(upd5)
                        cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd5), ctx.author.id))
                        db.commit()
                        await ctx.reply("YOU HAVE SUCCESSFULLY BOUGHT `mrvundela107rb` ICON CARD", file=discord.File(r'C:\Users\Admin\Desktop\Premier League bot\cards\mrvundela107rb.png'))
                    else:
                        await ctx.reply("one or more of those cards are in your lineup, remove them in order to claim your event") 
                else:
                    await ctx.reply("you do not have all the required items")
    else:
        await ctx.reply("Your card inventory is full")
    




### GAMING
@client.command(aliases=['m'])
@commands.cooldown(1,300,commands.BucketType.channel)
async def match(ctx, bet, opponent:discord.Member = None):
    if opponent == None:
        await ctx.reply("mention the person you are playing against")
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
    playershome = cursor.fetchone()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {opponent.id}")
    playersaway = cursor.fetchone()
    cursor.execute(f"SELECT balance FROM real WHERE user_id = {ctx.author.id}")
    wallethome = cursor.fetchone()
    cursor.execute(f"SELECT balance FROM real WHERE user_id = {opponent.id}")
    walletaway = cursor.fetchone()
    cursor.execute(f"SELECT * FROM packs WHERE user_id = {ctx.author.id}")
    packshome = cursor.fetchone()
    cursor.execute(f"SELECT * FROM packs WHERE user_id = {opponent.id}")
    packsaway = cursor.fetchone()

    button = Button(label="Play", style=discord.ButtonStyle.blurple)
    button2 = Button(label="Decline", style=discord.ButtonStyle.red)
    async def button_callback(interaction):
        if interaction.user.id == opponent.id:
            
            await interaction.response.edit_message(content="match accepted!", view=None)
            
            await ctx.send(f"MATCH BETWEEN <@{ctx.author.id}> and <@{opponent.id}> is starting........")
            await matchlineup(ctx.author.id, opponent.id)
            time.sleep(5)
            await ctx.send(file= discord.File("opponentlineup.png"))
            await ctx.send(file= discord.File("playerlineup.png"))

            i = 1
            n = 1
            totalovr1 = 0
            totalovr2 = 0
            
    
    


            while i != 12:
                player1 = playershome[i]
                playerovr1 = re.sub('\D', '', str(player1))
                totalovr1 = int(totalovr1) + int(playerovr1)
                i = i + 1
            while n != 12:
                player2 = playersaway[n]
                playerovr2 = re.sub('\D', '', str(player2))
                totalovr2 = int(totalovr2) + int(playerovr2)
                n = n + 1
            p1ovr = round(totalovr1/11)
            p2ovr = round(totalovr2/11)

            if p1ovr == p2ovr:
                chance1 = 30
                chance2 = 30
            if p1ovr > p2ovr:
                difference = p1ovr - p2ovr
                if difference > 30 :
                    chance1 = 4
                    chance2 = 60
                if 31 > difference > 15:
                    chance1 = 8
                    chance2 = 50
                if 16 > difference > 5:
                    chance1 = 20
                    chance2 = 40
                if 5 > difference > 0:
                    chance1 = 25
                    chance2 = 35 
                

            if p2ovr > p1ovr:
                difference = p2ovr - p1ovr
                if difference > 30 :
                    chance2 = 4
                    chance1 = 60
                if 31 > difference > 15:
                    chance2 = 8
                    chance1 = 50
                if 16 > difference > 5:
                    chance2 = 20
                    chance1 = 40
                if 5 > difference > 0:
                    chance2 = 25
                    chance1 = 35 
                
                
            embed = discord.Embed(title=f"{opponent.name} vs {ctx.author.name}", description=f"bet = {bet}:coin:\n\n{ctx.author} ovr = `{round(p1ovr)}` \n{opponent} ovr = `{round(p2ovr)}`.", color=discord.Color.red())
            embed.add_field(name=f"Pre-Match",value="no goals yet")
            await ctx.send(embed= embed)

            minute = 0
            p1goal = 0
            p2goal = 0

            while minute != 90:
                gc1 = random.randint(1,chance1)
                gc2 = random.randint(1,chance2)
                if gc1 == 1:
                    await ctx.send(f"🟥🟥🟥 {str(minute)}'  GOAL by `{playershome[random.randint(1,11)]}` for {ctx.author}🟥🟥🟥")
                    p1goal = p1goal + 1
                if gc2 == 1:
                    await ctx.send(f"🟦🟦🟦 {str(minute)}'  GOAL by `{playersaway[random.randint(1,11)]}` for {opponent}🟦🟦🟦")
                    p2goal = p2goal + 1
                if minute%10 == 1:
                    await ctx.send(f"`minute {minute}'`") 
                minute = minute + 1
                time.sleep(0.5)
                
                
            if minute == 90:
                if p1goal > p2goal:
                    winner = ctx.author.name
                    cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (wallethome[0] + int(bet), ctx.author.id))
                    cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (walletaway[0] - int(bet), opponent.id))
                    db.commit()
                if p2goal > p1goal:
                    winner = opponent.name
                    cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (wallethome[0] - int(bet), ctx.author.id))
                    cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (walletaway[0] + int(bet), opponent.id))
                    db.commit()
                if p2goal == p1goal:
                    winner = "no one"
                    




                await ctx.send(f"MATCH OVER `{p1goal} - {p2goal}`")
                embed2 = discord.Embed(title=f"{opponent.name} vs {ctx.author.name}", description=f"bet = {bet}:coin:\n\n{ctx.author} ovr = `{round(p1ovr)}` \n{opponent} ovr = `{round(p2ovr)}`.", color=discord.Color.red())
                embed2.add_field(name=f"Results",value=f"WINNER = {str(winner)}\n\n<@{ctx.author.id}> goals - {p1goal}\n<@{opponent.id}> goal - {p2goal}\n\n{winner} has received {bet} coins!!")
                await ctx.send(embed= embed2)
                bonus = random.randint(1,5)
                if bonus == 2:
                    await ctx.send("as a match bonus, both players get a `ucl pack`")
                    cursor.execute(f"UPDATE packs SET ucl = ? WHERE user_id = ?", (packshome[6] + 1, ctx.author.id))
                    cursor.execute(f"UPDATE packs SET ucl = ? WHERE user_id = ?", (packsaway[6] + 1, opponent.id))
                    db.commit()
                
                

        else:
            await interaction.response.send_message("this is not for you", ephemeral=True)
                
    async def button2_callback(interaction):
        if interaction.user.id == opponent.id:
            
            await interaction.response.edit_message(content="match declined!", view=None)
            await interaction.followup.send(f"<@{ctx.author.id}>, <@{opponent.id}> has declined your match offer")
            
        else:
            await interaction.response.send_message("this is not for you", ephemeral=True)
    button.callback = button_callback
    button2.callback = button2_callback
    view = View()
    view.add_item(button)
    view.add_item(button2)
    if ctx.author.id != opponent.id:
        if int(bet) >= 1000:
            if wallethome[0] >= int(bet) and walletaway[0] >= int(bet):
                if playershome[0] == 0 or playershome[1] == 0 or playershome[2] == 0 or playershome[3] == 0 or playershome[4] == 0 or playershome[5] == 0 or playershome[6] == 0 or playershome[7] == 0 or playershome[8] == 0 or playershome[9] == 0 or playershome[10] == 0 or playershome[11] == 0:
                    await ctx.reply("your lineup is not filled")
                else:
                    if playersaway[0] == 0 or playersaway[1] == 0 or playersaway[2] == 0 or playersaway[3] == 0 or playersaway[4] == 0 or playersaway[5] == 0 or playersaway[6] == 0 or playersaway[7] == 0 or playersaway[8] == 0 or playersaway[9] == 0 or playersaway[10] == 0 or playersaway[11] == 0:
                        await ctx.reply("opponents lineup is not filled")
                    else:
                        await ctx.send(f"<@{opponent.id}>, <@{ctx.author.id}> has challenged you to a match for `{bet}` coins‼️‼️, press play to confirm",view=view)
                        
            else:
                await ctx.reply("you or the oppenent does not have enough money for the bet")
        else:
            await ctx.reply("you have to bet atleast a 1000 coins for a game")
    else:
        await ctx.reply("you cant play a match against yourself")
    




async def matchlineup(user, opponent):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {user}")
    playershome = cursor.fetchone()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {opponent}")
    playersaway = cursor.fetchone()

    field = Image.open("lineup.png")
        
    st = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[1]}.png')
    st = st.resize((170,220))
    gk = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[2]}.png')
    gk = gk.resize((170,220))
    cb1 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[3]}.png')
    cb1 = cb1.resize((170,220))
    cb2 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[4]}.png')
    cb2 = cb2.resize((170,220))
    lb = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[5]}.png')
    lb = lb.resize((170,220))
    rb = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[6]}.png')
    rb = rb.resize((170,220))
    cm1 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[7]}.png')
    cm1 = cm1.resize((170,220))
    cm2 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[8]}.png')
    cm2 = cm2.resize((170,220))
    cm3 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[9]}.png')
    cm3 = cm3.resize((170,220))
    lw = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[10]}.png')
    lw = lw.resize((170,220))
    rw = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playershome[11]}.png')
    rw = rw.resize((170,220))
        

    field.paste(gk, (515,450), gk)
    field.paste(cb1, (315,350), cb1)
    field.paste(cb2, (715,350), cb2)
    field.paste(cm2, (515,200), cm2)
    field.paste(cm1, (130,200), cm1)
    field.paste(cm3, (900,200), cm3)
    field.paste(st, (515,0), st)
    field.paste(lw, (130,0), lw)
    field.paste(rw, (900,0), rw)  
    field.paste(lb, (30,400), lb)
    field.paste(rb, (1000,400), rb)  
        


    field.save("playerlineup.png")

    field2 = Image.open("lineup.png")
        
    _st = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[1]}.png')
    _st = _st.resize((170,220)).rotate(180)
    _gk = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[2]}.png')
    _gk = _gk.resize((170,220)).rotate(180)
    _cb1 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[3]}.png')
    _cb1 = _cb1.resize((170,220)).rotate(180)
    _cb2 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[4]}.png')
    _cb2 = _cb2.resize((170,220)).rotate(180)
    _lb = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[5]}.png')
    _lb = _lb.resize((170,220)).rotate(180)
    _rb = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[6]}.png')
    _rb = _rb.resize((170,220)).rotate(180)
    _cm1 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[7]}.png')
    _cm1 = _cm1.resize((170,220)).rotate(180)
    _cm2 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[8]}.png')
    _cm2 = _cm2.resize((170,220)).rotate(180)
    _cm3 = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[9]}.png')
    _cm3 = _cm3.resize((170,220)).rotate(180)
    _lw = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[10]}.png')
    _lw = _lw.resize((170,220)).rotate(180)
    _rw = Image.open(rf'C:\Users\Admin\Desktop\Premier League bot\cards\{playersaway[11]}.png')
    _rw = _rw.resize((170,220)).rotate(180)
        

    field2.paste(_gk, (515,450), _gk)
    field2.paste(_cb1, (315,350), _cb1)
    field2.paste(_cb2, (715,350), _cb2)
    field2.paste(_cm2, (515,200), _cm2)
    field2.paste(_cm1, (130,200), _cm1)
    field2.paste(_cm3, (900,200), _cm3)
    field2.paste(_st, (515,0), _st)
    field2.paste(_lw, (130,0), _lw)
    field2.paste(_rw, (900,0), _rw)  
    field2.paste(_lb, (30,400), _lb)
    field2.paste(_rb, (1000,400), _rb)  
        


    field2.save("opponentlineupstraight.png")

    p2 = Image.open("opponentlineupstraight.png")
    p2 = p2.rotate(180)
    p2.save("opponentlineup.png")


@client.command(aliases=['lb'])
async def leaderboard(ctx):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM best")
    lbdata = cursor.fetchall()
    print(lbdata)
    highestovrs = sorted(lbdata, reverse=True)
    embed = discord.Embed(title=f"`OVR Leaderboard`", description=f"Players with the highest ovrs. (do `.team` to refresh your ovrs)", color=discord.Color.green())
    i = 0
    embed.add_field(name=f"**Top 10**",value="")
    while i != 10:
        user = highestovrs[i]
        if user[1] == 583246523664433162:
            embed.add_field(name=f"",value=f"{i+1}. ⭐<@{user[1]}>⭐ - OVR `{user[0]}`", inline=False)
        else:
            embed.add_field(name=f"",value=f"{i+1}. <@{user[1]}> - OVR `{user[0]}`", inline=False)
        i = i + 1
        

    
    await ctx.send(embed= embed)
    




@client.command()
async def give(ctx, card, user:discord.Member = None):
    if user == None:
        await ctx.send("mention user to give card")
    if user.id == ctx.author.id:
        await ctx.send("you cant give yourself something")
    else:
        db = sqlite3.connect("real.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
        cards = cursor.fetchone()
        cursor.execute(f"SELECT * FROM toty WHERE user_id = {user.id}")
        cardsrec = cursor.fetchone()
        print(cards)
        if(str(card) in str(cards)):
            if(str(card) in str(cardsrec)):
                await ctx.reply("the person already has this card")
            else:
                lc = await lineupcheck(card, ctx.author.id)
                if lc == True:
                    await ctx.reply("you cant give cards that are in your lineup, do `.remove [pos]` to remove it")
                if lc == False:
                    async def button_callback(interaction):
                        if interaction.user.id == user.id:
                            _c1 = f"{card}, "
                            upd0 = str(cards[1]) + ", "
                            upd1 = str(upd0).replace(_c1, "")                
                            upd2 = str(upd1[:-2])   
                            c2 = f", {card}"                    
                            await interaction.response.edit_message(content=f"accepted by <@{interaction.user.id}>",view=None)
                            cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd2), ctx.author.id))
                            cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(cardsrec[1]) + str(c2), user.id))
                            db.commit()
                        else:
                            await interaction.response.send_message("this isnt for you biatch",ephemeral=True)


                    button = Button(label="Yes", style=discord.ButtonStyle.green)
                    button.callback = button_callback

                    view = View()
                    view.add_item(button)

                    await ctx.reply(f"<@{user.id}>, do you want `{card}` given by <@{ctx.author.id}>?",view=view)
                    
        else:
            await ctx.reply("you dont have that card")


@client.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def setup(ctx):
    global strikers
    global goalkeepers
    global centrebacks
    global leftbacks
    global rightbacks
    global midfielders
    global leftwings
    global rightwings
    global stcard
    global lwcard
    global rwcard
    global cm1card
    global cm2card
    global cm3card
    global lbcard
    global cb1card
    global cb2card
    global rbcard
    global gkcard
    stcard = 0
    lwcard = 0
    rwcard = 0
    cm1card = 0
    cm2card = 0
    cm3card = 0
    lbcard = 0
    cb1card = 0
    cb2card = 0
    rbcard = 0
    gkcard = 0


    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
    allpos = cursor.fetchone()
    card_list = [None, "cards"]
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    cards = cursor.fetchone()
    cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, cards)]
    cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
    finalcards = cards_[30:]
    fcl = finalcards.split(', ')
    i = 0



    stlist = []
    lwlist = []
    rwlist = []
    midfielderlist = []
    lblist = []
    rblist = []
    cblist = []
    gklist = []


    while i != len(fcl): #len(fcl) is no of cards
        optioncard = fcl[i]
        if(str(optioncard) in strikers):
            stlist.append(discord.SelectOption(label=optioncard))
        if(str(optioncard) in leftwings):
            lwlist.append(discord.SelectOption(label=optioncard))
        if(str(optioncard) in rightwings):
            rwlist.append(discord.SelectOption(label=optioncard))
        if(str(optioncard) in midfielders):
            midfielderlist.append(discord.SelectOption(label=optioncard))
        if(str(optioncard) in leftbacks):
            lblist.append(discord.SelectOption(label=optioncard))
        if(str(optioncard) in rightbacks):
            rblist.append(discord.SelectOption(label=optioncard))
        if(str(optioncard) in centrebacks):
            cblist.append(discord.SelectOption(label=optioncard))
        if(str(optioncard) in goalkeepers):
            gklist.append(discord.SelectOption(label=optioncard))
        i = i + 1
        print(i)
  
    if len(stlist) == 0:
        selectst = Select(placeholder="You do not have any strikers",options=[discord.SelectOption(label="0")])
    else:
        selectst = Select(options=stlist,placeholder="strikers⭕")
    if len(lwlist) == 0:
        selectlw = Select(placeholder="You do not have any left wings",options=[discord.SelectOption(label="0")])
    else:
        selectlw = Select(options=lwlist,placeholder="left wings⭕")
    if len(rwlist) == 0:
        selectrw = Select(placeholder="You do not have any right wings",options=[discord.SelectOption(label="0")])
    else:
        selectrw = Select(options=rwlist,placeholder="right wings⭕")
    if len(midfielderlist) == 0:
        selectcm1 = Select(placeholder="You do not have any midfielders",options=[discord.SelectOption(label="0")])
    else:
        selectcm1 = Select(options=midfielderlist,placeholder="centre mid 1⭕")
    if len(midfielderlist) == 0:
        selectcm2 = Select(placeholder="You do not have any midfielders",options=[discord.SelectOption(label="0")])
    else:
        selectcm2 = Select(options=midfielderlist,placeholder="centre mid 2⭕")
    if len(midfielderlist) == 0:
        selectcm3 = Select(placeholder="You do not have any midfielders",options=[discord.SelectOption(label="0")])
    else:
        selectcm3 = Select(options=midfielderlist,placeholder="centre mid 3⭕")
    if len(lblist) == 0:
        selectlb = Select(placeholder="You do not have any leftbacks",options=[discord.SelectOption(label="0")])
    else:
        selectlb = Select(options=lblist,placeholder="left backs⭕")
    if len(rblist) == 0:
        selectrb = Select(placeholder="You do not have any rightbacks",options=[discord.SelectOption(label="0")])
    else:
        selectrb = Select(options=rblist,placeholder="right backs⭕")
    if len(cblist) == 0:
        selectcb1 = Select(placeholder="You do not have any centrebacks",options=[discord.SelectOption(label="0")])
    else:
        selectcb1 = Select(options=cblist,placeholder="centre back 1⭕")
    if len(cblist) == 0:
        selectcb2 = Select(placeholder="You do not have any centrebacks",options=[discord.SelectOption(label="0")])
    else:
        selectcb2 = Select(options=cblist,placeholder="centre back 2⭕")
    if len(gklist) == 0:
        selectgk = Select(placeholder="You do not have any goalkeepers",options=[discord.SelectOption(label="0")])
    else:
        selectgk = Select(options=gklist,placeholder="goalkeepers⭕")
    
    
    
    async def stcallback(interaction):
        if interaction.user.id == ctx.author.id:
            global stcard
            stcard = str(selectst.values[0])
            await interaction.response.send_message(f"striker set to `{stcard}`")             
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def lwcallback(interaction):
        if interaction.user.id == ctx.author.id:
            global lwcard
            lwcard = str(selectlw.values[0])
            await interaction.response.send_message(f"left wing set to `{lwcard}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def rwcallback(interaction):
        if interaction.user.id == ctx.author.id:
            global rwcard
            rwcard = str(selectrw.values[0])
            await interaction.response.send_message(f"right wing set to `{rwcard}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def cm1callback(interaction):
        if interaction.user.id == ctx.author.id:
            global cm1card
            cm1card = str(selectcm1.values[0])
            await interaction.response.send_message(f"centre mid 1 set to `{cm1card}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def cm2callback(interaction):
        if interaction.user.id == ctx.author.id:
            global cm2card
            cm2card = str(selectcm2.values[0])
            await interaction.response.send_message(f"centre mid 2 set to `{cm2card}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def cm3callback(interaction):
        if interaction.user.id == ctx.author.id:
            global cm3card
            cm3card = str(selectcm3.values[0])
            await interaction.response.send_message(f"centre mid 3 set to `{cm3card}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def lbcallback(interaction):
        if interaction.user.id == ctx.author.id:
            global lbcard
            lbcard = str(selectlb.values[0])
            await interaction.response.send_message(f"left back set to `{lbcard}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def rbcallback(interaction):
        if interaction.user.id == ctx.author.id:
            global rbcard
            rbcard = str(selectrb.values[0])
            await interaction.response.send_message(f"right back set to `{rbcard}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def cb1callback(interaction):
        
        if interaction.user.id == ctx.author.id:
            global cb1card
            cb1card = str(selectcb1.values[0])
            await interaction.response.send_message(f"centre back 1 set to `{cb1card}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def cb2callback(interaction):
        if interaction.user.id == ctx.author.id:
            global cb2card
            cb2card = str(selectcb2.values[0])
            await interaction.response.send_message(f"centre back 2 set to `{cb2card}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    async def gkcallback(interaction):
        if interaction.user.id == ctx.author.id:
            global gkcard
            gkcard = str(selectgk.values[0])
            await interaction.response.send_message(f"goalkeeper set to `{gkcard}`")
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    
    denybutton = Button(label="Default", style=discord.ButtonStyle.red, emoji = "⛔")
    async def denybutton_callback(interaction):
        if interaction.user.id == ctx.author.id:
            await interaction.response.edit_message(content="`no changes`",view=None)
            await ctx.send("Select your midfielders `cm1` `cm2` and `cm3`",view=view2) # msg 2
        else:
            await interaction.response.send_messege(f"{interaction.author} this is not for you")
    denybutton2 = Button(label="Default", style=discord.ButtonStyle.red, emoji = "⛔")
    async def denybutton2_callback(interaction):
        if interaction.user.id == ctx.author.id:
            await interaction.response.edit_message(content="`no changes`",view=None)
            await ctx.send("Select your defense `lb` `rb` `cb1` and `cb2`",view=view3) #msg 3
          
        else:
            await interaction.response.send_messege(f"{interaction.author} this is not for you")
    denybutton3 = Button(label="Default", style=discord.ButtonStyle.red, emoji = "⛔")
    async def denybutton3_callback(interaction):
        if interaction.user.id == ctx.author.id:
            await interaction.response.edit_message(content="`no changes`",view=None)
        else:
            await interaction.response.send_messege(f"{interaction.author} this is not for you")




    button = Button(label="Save Changes", style=discord.ButtonStyle.green, emoji = "✔️")
    async def button_callback(interaction):
        if interaction.user.id == ctx.author.id:
            global stcard
            global lwcard
            global rwcard
            global gkcard
            db = sqlite3.connect("real.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
            allpos = cursor.fetchone()
            
            if str(lwcard) == str(allpos[5]) != str(0) or str(lwcard) == str(allpos[7]) != str(0) or str(rwcard) == str(allpos[6]) != str(0) or str(rwcard) == str(allpos[9]) != str(0):
                await interaction.response.send_message("one or multiple of those cards are placed in the lineup somewhere else")
                cursor.close()
                db.close()
            
            else:
                global phase
                await interaction.response.edit_message(content="`saved changes`",view=None)
                cursor.execute(f"UPDATE team SET st = ? WHERE user_id = ?", (stcard, ctx.author.id))
                cursor.execute(f"UPDATE team SET gk = ? WHERE user_id = ?", (gkcard, ctx.author.id))
                cursor.execute(f"UPDATE team SET lw = ? WHERE user_id = ?", (lwcard, ctx.author.id))
                cursor.execute(f"UPDATE team SET rw = ? WHERE user_id = ?", (rwcard, ctx.author.id))
                db.commit()
                cursor.close()
                db.close()
                #msg 2
                await ctx.send("Select your midfielders `cm1` `cm2` and `cm3`",view=view2)

                
            
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    
    button2 = Button(label="Save Changes", style=discord.ButtonStyle.green, emoji = "✔️")
    async def button2_callback(interaction):
        if interaction.user.id == ctx.author.id:
            global cm1card
            global cm2card
            global cm3card
            db = sqlite3.connect("real.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
            allpos = cursor.fetchone()
            
            if str(cm1card) == str(allpos[10]) != str(0) or str(cm1card) == str(allpos[5]) != str(0) or str(cm3card) == str(allpos[11]) != str(0) or str(cm3card) == str(allpos[6]) != str(0) or str(cm1card) == str(allpos[8]) != str(0) or str(cm1card) == str(allpos[9]) != str(0) or str(cm2card) == str(allpos[7]) != str(0) or str(cm2card) == str(allpos[9]) != str(0) or str(cm3card) == str(allpos[8]) != str(0) or str(cm3card) == str(allpos[7]) != str(0):
                await interaction.response.send_message("one or multiple of those cards are placed in the lineup somewhere else")
                cursor.close()
                db.close()
                
            else:
                if str(cm1card) == str(cm2card) != str(0) or str(cm2card) == str(cm3card) != str(0) or str(cm3card) == str(cm1card) != str(0):
                    await interaction.response.send_message("you cannot choose the same card for multiple positions")
                    cursor.close()
                    db.close()
                else:

                    await interaction.response.edit_message(content="`saved changes`",view=None)
                    cursor.execute(f"UPDATE team SET cm1 = ? WHERE user_id = ?", (cm1card, ctx.author.id))
                    cursor.execute(f"UPDATE team SET cm2 = ? WHERE user_id = ?", (cm2card, ctx.author.id))
                    cursor.execute(f"UPDATE team SET cm3 = ? WHERE user_id = ?", (cm3card, ctx.author.id))

                    db.commit()
                    cursor.close()
                    db.close()
                    #msg 3
                    await ctx.send("Select your defense `lb` `rb` `cb1` and `cb2`",view=view3)

            
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")
    
    button3 = Button(label="Save Changes", style=discord.ButtonStyle.green, emoji = "✔️")
    async def button3_callback(interaction):
        if interaction.user.id == ctx.author.id:
            global lbcard
            global rbcard
            global cb1card
            global cb2card
            db = sqlite3.connect("real.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
            allpos = cursor.fetchone()
            
            if str(lbcard) == str(allpos[10]) != str(0) or str(lbcard) == str(allpos[7]) != str(0) or str(rbcard) == str(allpos[11]) != str(0) or str(rwcard) == str(allpos[9]) != str(0):
                await interaction.response.send_message("one or multiple of those cards are placed in the lineup somewhere else")
                cursor.close()
                db.close()
            else:
                if str(cb1card) == str(cb2card) != str(0):
                    await interaction.response.send_message("you cannot choose the same card for multiple positions")
                    cursor.close()
                    db.close()
                else:
                    await interaction.response.edit_message(content="`saved changes`",view=None)
                    cursor.execute(f"UPDATE team SET lb = ? WHERE user_id = ?", (lbcard, ctx.author.id))
                    cursor.execute(f"UPDATE team SET rb = ? WHERE user_id = ?", (rbcard, ctx.author.id))
                    cursor.execute(f"UPDATE team SET cb1 = ? WHERE user_id = ?", (cb1card, ctx.author.id))
                    cursor.execute(f"UPDATE team SET cb2 = ? WHERE user_id = ?", (cb2card, ctx.author.id))
                    db.commit()
                    cursor.close()
                    db.close()
            
        else:
            await ctx.message.send(f"@<{ctx.author.id}> this is not for you")

        
    button.callback = button_callback
    button2.callback = button2_callback
    button3.callback = button3_callback
    denybutton.callback = denybutton_callback
    denybutton2.callback = denybutton2_callback
    denybutton3.callback = denybutton3_callback

    selectst.callback = stcallback
    selectlw.callback = lwcallback
    selectrw.callback = rwcallback
    selectcm1.callback = cm1callback
    selectcm2.callback = cm2callback
    selectcm3.callback = cm3callback
    selectlb.callback = lbcallback
    selectrb.callback = rbcallback
    selectcb1.callback = cb1callback
    selectcb2.callback = cb2callback
    selectgk.callback = gkcallback

    view = View()
    view2 = View()
    view3 = View()
    view.add_item(selectst)
    view.add_item(selectlw)
    view.add_item(selectrw)
    view.add_item(selectgk)
    view.add_item(button)
    view.add_item(denybutton)
    view2.add_item(selectcm1)
    view2.add_item(selectcm2)
    view2.add_item(selectcm3)
    view2.add_item(button2)
    view2.add_item(denybutton2)
    view3.add_item(selectlb)
    view3.add_item(selectrb)
    view3.add_item(selectcb1)
    view3.add_item(selectcb2)
    view3.add_item(button3)
    view3.add_item(denybutton3)
    
    if i == len(fcl):
        await ctx.reply("Select your forwards `st` `lw` `rw` and goalkeeper `gk`",view=view)

        
    
        










        
@client.command()
async def pens(ctx, bet, user:discord.Member = None):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    if user == None:
        await ctx.reply("mention someone to play against")
    if user.id == ctx.author.id:
        await ctx.send("you cant play with yourself")
    else:
        cursor.execute(f"SELECT * FROM team WHERE user_id = {ctx.author.id}")
        allpos1 = cursor.fetchone()
        cursor.execute(f"SELECT * FROM team WHERE user_id = {user.id}")
        allpos2 = cursor.fetchone()
        shooterhome = allpos1[1]
        shooteraway = allpos2[1]
        keeperaway = allpos2[2]
        keeperhome = allpos1[2]
        print(shooteraway)
        




# MARKET MARK

@client.command(aliases=['sm'])
async def sellmarket(ctx, slot=None, card=None, cost=None):
    card_list = [None, "cards"]

    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    ownedcards = cursor.fetchone()
    cards_ = [f"{i} {j}" for i, j in itertools.zip_longest(card_list, ownedcards)]
    cards_ = "\n".join(cards_) if len(cards_) > 0 else "*No cards in inventory*"
    finalcards = cards_[30:]
    fcl = finalcards.split(', ')
    fcl.sort()
    olist = []
    i = 0
    if slot == None:
        #slot number select
        select = Select(placeholder="1️Choose A Slot Number",options=[
                discord.SelectOption(label="s1"),discord.SelectOption(label="s2"),discord.SelectOption(label="s3"),discord.SelectOption(label="s4"),discord.SelectOption(label="s5")
            ])
        # select card
        while i != len(fcl)-1:
            optioncard = fcl[i]
            check1 = await lineupcheck(optioncard, ctx.author.id)
            if check1 == False:
                if(str(optioncard) in basecards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟫"))
                if(str(optioncard) in totwcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟧"))
                if(str(optioncard) in futurecards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟪"))
                if(str(optioncard) in totycards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟦"))
                if(str(optioncard) in alliconcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟨"))
                if(str(optioncard) in uclcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="🟩"))
                if(str(optioncard) in totscards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="⬛"))
                if(str(optioncard) in specialcards):
                    olist.append(discord.SelectOption(label=optioncard,emoji="♦"))
            i = i + 1
        select2 = Select(placeholder="Choose selling card",options=olist)
        # select price
        select3 = Select(placeholder="Choose A Price",options=[
                discord.SelectOption(label="200"),discord.SelectOption(label="400"),discord.SelectOption(label="600"),discord.SelectOption(label="800"),discord.SelectOption(label="1000"),discord.SelectOption(label="1500"),discord.SelectOption(label="2000"),discord.SelectOption(label="2500"),discord.SelectOption(label="3000")
            ])
        async def callback1(interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.response.edit_message(content="2️⃣Select Card",view=view2)
            else:
                await interaction.response.send_message("this is not for you", ephemeral=True)
        async def callback2(interaction):
            if interaction.user.id == ctx.author.id:
                await interaction.response.edit_message(content="3️⃣Select Card Price (for a custom price, run command manually)",view=view3)
            else:
                await interaction.response.send_message("this is not for you", ephemeral=True)
        async def callback3(interaction):
            if interaction.user.id == ctx.author.id:
                slotno = select.values[0]
                card = select2.values[0]
                cost = select3.values[0]
                cursor.execute(f"UPDATE pmarket SET {slotno} = ? WHERE user_id = ?", (str(card), ctx.author.id))
                cursor.execute(f"UPDATE pmarket SET c{str(slotno[1:])} = ? WHERE user_id = ?", (int(cost), ctx.author.id))               
                upd0 = str(ownedcards[1]) + ", "
                upd1 = str(upd0).replace(f"{card}, ", "")
                upd2 = str(upd1[:-2])
                print(upd2)
                cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd2), ctx.author.id))
                await ctx.reply(f"🔷your card `{card}` is selling for {int(cost)}:coin: in {slotno}")
                db.commit()
                await interaction.response.edit_message(content=f"sold `{select2.values[0]}`",view=None)
            else:
                await interaction.response.send_message("this is not for you", ephemeral=True)
        select.callback = callback1
        select2.callback = callback2
        select3.callback = callback3
        view1 = View()
        view2 = View()
        view3 = View()
        view1.add_item(select)
        view2.add_item(select2)
        view3.add_item(select3)

        await ctx.reply("1️⃣Select Your Market Slot",view=view1)
















    else:
        check1 = await ownershipcheck(card, ctx.author.id)
        if check1 == True:
            check2 = await lineupcheck(card, ctx.author.id)
            if check2 == True:
                await ctx.reply("cards in your lineup cannot be sold.")
            else:
                if slot == "s1":
                    cursor.execute(f"UPDATE pmarket SET s1 = ? WHERE user_id = ?", (str(card), ctx.author.id))
                    cursor.execute(f"UPDATE pmarket SET c1 = ? WHERE user_id = ?", (int(cost), ctx.author.id))               
                    upd0 = str(ownedcards[1]) + ", "
                    upd1 = str(upd0).replace(f"{card}, ", "")
                    upd2 = str(upd1[:-2])
                    print(upd2)
                    cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd2), ctx.author.id))
                    await ctx.reply(f"🔷your card `{card}` is selling for {int(cost)}:coin: in slot 1")
                    db.commit()
                if slot == "s2":
                    cursor.execute(f"UPDATE pmarket SET s2 = ? WHERE user_id = ?", (str(card), ctx.author.id))
                    cursor.execute(f"UPDATE pmarket SET c2 = ? WHERE user_id = ?", (int(cost), ctx.author.id))
                    upd0 = str(ownedcards[1]) + ", "
                    upd1 = str(upd0).replace(f"{card}, ", "")
                    upd2 = str(upd1[:-2])
                    cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd2), ctx.author.id))
                    await ctx.reply(f"🔷your card `{card}` is selling for {int(cost)}:coin: in slot 2")
                    db.commit()
                if slot == "s3":
                    cursor.execute(f"UPDATE pmarket SET s3 = ? WHERE user_id = ?", (str(card), ctx.author.id))
                    cursor.execute(f"UPDATE pmarket SET c3 = ? WHERE user_id = ?", (int(cost), ctx.author.id))
                    upd0 = str(ownedcards[1]) + ", "
                    upd1 = str(upd0).replace(f"{card}, ", "")
                    upd2 = str(upd1[:-2])
                    cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd2), ctx.author.id))
                    await ctx.reply(f"🔷your card `{card}` is selling for {int(cost)}:coin: in slot 3")
                    db.commit()
                if slot == "s4":
                    cursor.execute(f"UPDATE pmarket SET s4 = ? WHERE user_id = ?", (str(card), ctx.author.id))
                    cursor.execute(f"UPDATE pmarket SET c4 = ? WHERE user_id = ?", (int(cost), ctx.author.id))
                    upd0 = str(ownedcards[1]) + ", "
                    upd1 = str(upd0).replace(f"{card}, ", "")
                    upd2 = str(upd1[:-2])
                    cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd2), ctx.author.id))
                    await ctx.reply(f"🔷your card `{card}` is selling for {int(cost)}:coin: in slot 4")
                    db.commit()
                if slot == "s5":
                    cursor.execute(f"UPDATE pmarket SET s5 = ? WHERE user_id = ?", (str(card), ctx.author.id))
                    cursor.execute(f"UPDATE pmarket SET c5 = ? WHERE user_id = ?", (int(cost), ctx.author.id))
                    upd0 = str(ownedcards[1]) + ", "
                    upd1 = str(upd0).replace(f"{card}, ", "")
                    upd2 = str(upd1[:-2])
                    cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd2), ctx.author.id))
                    await ctx.reply(f"🔷your card `{card}` is selling for {int(cost)}:coin: in slot 5")
                    db.commit()

        else:
            await ctx.reply("you do not own this card")








@client.command(aliases=['mar'])
async def market(ctx, user:discord.Member = None):
    global ownedcards
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT balance FROM real WHERE user_id = {ctx.author.id}")
    wallet = cursor.fetchone()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    ownedcards = cursor.fetchone()

    i = 1
    n = 1
    if user == None or user.id == ctx.author.id:
        cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {ctx.author.id}")
        usermarket = cursor.fetchone()
        embed = discord.Embed(title=f"`Your Market`", description=f"check `.marketinfo` for info on how to use market", color=discord.Color.yellow())
        embed.add_field(name=f"**SLOT 1**",value=f"🔻`{usermarket[1]}` --- {usermarket[2]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 2**",value=f"🔻`{usermarket[3]}` --- {usermarket[4]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 3**",value=f"🔻`{usermarket[5]}` --- {usermarket[6]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 4**",value=f"🔻`{usermarket[7]}` --- {usermarket[8]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 5**",value=f"🔻`{usermarket[9]}` --- {usermarket[10]}:coin: ", inline=False)

        await ctx.send(embed= embed)
    else:
        cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {user.id}")
        usermarket = cursor.fetchone()
        embed = discord.Embed(title=f"`{user}'s Market`", description=f"check `.marketinfo` for info on how to use market", color=discord.Color.yellow())
        embed.add_field(name=f"**SLOT 1**",value=f"🔻`{usermarket[1]}` --- {usermarket[2]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 2**",value=f"🔻`{usermarket[3]}` --- {usermarket[4]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 3**",value=f"🔻`{usermarket[5]}` --- {usermarket[6]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 4**",value=f"🔻`{usermarket[7]}` --- {usermarket[8]}:coin: ", inline=False)
        embed.add_field(name=f"**SLOT 5**",value=f"🔻`{usermarket[9]}` --- {usermarket[10]}:coin: ", inline=False)

        olist = []
        
        while n != 6: 
            print(n)
            if usermarket[i] != 0:
                olist.append(discord.SelectOption(label=f"Slot {n}",emoji="🟫"))
            n = n + 1
            i = i + 2
           
        if len(olist) == 0:
            select = Select(placeholder="Their shop is empty",options=[
                discord.SelectOption(label="close shop")
            ])
        else:
            select = Select(placeholder="💰BUY💰",options=olist)

        async def my_callback(interaction):
            global ownedcards
            if interaction.user.id == ctx.author.id:
                if select.values[0] == "close shop":
                    await interaction.response.edit_message(content="shop closed",view=None)
                else:
                    await interaction.response.edit_message(content=f"you have selected `{select.values[0]}`", view=None)

                    if str(select.values[0]) == "Slot 1":
                        scard = usermarket[1]
                        price = usermarket[2]
                        slotno = "1"
                    if str(select.values[0]) == "Slot 2":
                        scard = usermarket[3]
                        price = usermarket[4]
                        slotno = "2"
                    if str(select.values[0]) == "Slot 3":
                        scard = usermarket[5]
                        price = usermarket[6]
                        slotno = "3"
                    if str(select.values[0]) == "Slot 4":
                        scard = usermarket[7]
                        price = usermarket[8]
                        slotno = "4"
                    if str(select.values[0]) == "Slot 5":
                        scard = usermarket[9]
                        price = usermarket[10]
                        slotno = "5"
                    
                    ocheck = await ownershipcheck(str(scard),ctx.author.id)
                    if ocheck == True:
                        await ctx.reply("you already have this card")
                    else:
                        fullcheck = await invfullcheck(ctx.author.id)
                        if fullcheck == False:
                            if int(wallet[0]) < int(usermarket[2]):
                                await ctx.reply("you do not have enough :coin: for the purchase")
                            else:
                                cursor.execute(f"UPDATE pmarket SET s{str(slotno)} = ? WHERE user_id = ?", (0, user.id))
                                cursor.execute(f"UPDATE pmarket SET c{str(slotno)} = ? WHERE user_id = ?", (0, user.id))
                                cursor.execute(f"UPDATE real SET balance = ? WHERE user_id = ?", (wallet[0] - price, ctx.author.id))
                                upd0 = str(ownedcards[1]) + f", {scard}"
                                cursor.execute("UPDATE toty SET cards = ? WHERE user_id = ?", (str(upd0), ctx.author.id))
                                await ctx.reply(f"you have bought {select.values[0]} of <@{user.id}>'s market for {price}:coin:")
                                db.commit()
                                await user.send(f"<@{ctx.author.id}> has bought your `{scard}` for {price}:coin: from slot number {slotno}")
                        else:
                            await ctx.reply("Your card inventory is full")
                    


                
            else:
                await ctx.send(f"@<{ctx.author.id}> this is not for you")


        select.callback = my_callback
        view = View()
        view.add_item(select)

        if n == 6:
            await ctx.reply(embed=embed,view=view)

@client.command(aliases=['tm'])
async def topmarket(ctx):

    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM best")
    lbdata = cursor.fetchall()
    
    highestovrs = sorted(lbdata, reverse=True)
    lbuser1 = highestovrs[0]
    print(lbuser1)
    lbuser2 = highestovrs[1]
    lbuser3 = highestovrs[2]
    lbuser4 = highestovrs[3]
    lbuser5 = highestovrs[4]

    cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {lbuser1[1]}")
    usermarket = cursor.fetchone()
    cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {lbuser2[1]}")
    usermarket2 = cursor.fetchone()
    cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {lbuser3[1]}")
    usermarket3 = cursor.fetchone()
    cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {lbuser4[1]}")
    usermarket4 = cursor.fetchone()
    cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {lbuser5[1]}")
    usermarket5 = cursor.fetchone()

    embed = discord.Embed(title=f"`Markets of the Top 5 players`", description=f"check `.marketinfo` for info on how to use market", color=discord.Color.orange())
    embed.add_field(name=f"Top 1",value=f"<@{lbuser1[1]}>'s market🔴\nslot1 - `{usermarket[1]}` --- {usermarket[2]}:coin:\nslot2 - `{usermarket[3]}` --- {usermarket[4]}:coin:\nslot3 - `{usermarket[5]}` --- {usermarket[6]}:coin:\nslot4 - `{usermarket[7]}` --- {usermarket[8]}:coin:\nslot5 - `{usermarket[9]}` --- {usermarket[10]}:coin:",inline=False)
    embed.add_field(name=f"Top 2",value=f"<@{lbuser2[1]}>'s market🟠\nslot1 - `{usermarket2[1]}` --- {usermarket2[2]}:coin:\nslot2 - `{usermarket2[3]}` --- {usermarket2[4]}:coin:\nslot3 - `{usermarket2[5]}` --- {usermarket2[6]}:coin:\nslot4 - `{usermarket2[7]}` --- {usermarket2[8]}:coin:\nslot5 - `{usermarket2[9]}` --- {usermarket2[10]}:coin:",inline=False)
    embed.add_field(name=f"Top 3",value=f"<@{lbuser3[1]}>'s market🟡\nslot1 - `{usermarket3[1]}` --- {usermarket3[2]}:coin:\nslot2 - `{usermarket3[3]}` --- {usermarket3[4]}:coin:\nslot3 - `{usermarket3[5]}` --- {usermarket3[6]}:coin:\nslot4 - `{usermarket3[7]}` --- {usermarket3[8]}:coin:\nslot5 - `{usermarket3[9]}` --- {usermarket3[10]}:coin:",inline=False)
    embed.add_field(name=f"Top 4",value=f"<@{lbuser4[1]}>'s market🟢\nslot1 - `{usermarket4[1]}` --- {usermarket4[2]}:coin:\nslot2 - `{usermarket4[3]}` --- {usermarket4[4]}:coin:\nslot3 - `{usermarket4[5]}` --- {usermarket4[6]}:coin:\nslot4 - `{usermarket4[7]}` --- {usermarket4[8]}:coin:\nslot5 - `{usermarket4[9]}` --- {usermarket4[10]}:coin:",inline=False)
    embed.add_field(name=f"Top 5",value=f"<@{lbuser5[1]}>'s market🔵\nslot1 - `{usermarket5[1]}` --- {usermarket5[2]}:coin:\nslot2 - `{usermarket5[3]}` --- {usermarket5[4]}:coin:\nslot3 - `{usermarket5[5]}` --- {usermarket5[6]}:coin:\nslot4 - `{usermarket5[7]}` --- {usermarket5[8]}:coin:\nslot5 - `{usermarket5[9]}` --- {usermarket5[10]}:coin:",inline=False)
    await ctx.send(embed= embed)

@client.command(aliases=['rm'])
async def randommarket(ctx):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM pmarket")
    usermarket = cursor.fetchall()
    i = 1
    markets = []
    cardslots = [1, 3, 5, 7, 9]
    while len(markets) != 5:
        tempmarket = random.randint(0,len(usermarket) - 1)
        rm = usermarket[tempmarket]
        n = random.choice(cardslots)
        if rm[n] != 0:
            markets.append(f"`{rm[n]}` - {rm[n+1]}:coin: by <@{rm[0]}>")
    if len(markets) == 5:
        embed = discord.Embed(title=f"`Random Markets`", description=f"check `.marketinfo` for info on how to use market", color=discord.Color.magenta())
        embed.add_field(name=f"Random slots of random player's markets",value=f"{markets[0]}\n{markets[1]}\n{markets[2]}\n{markets[3]}\n{markets[4]}\n",inline=False)
        await ctx.reply(embed= embed)

@client.command()
async def clearslot(ctx, slot):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM pmarket WHERE user_id = {ctx.author.id}")
    usermarket = cursor.fetchone()

    slots = ['s1','s2','s3','s4','s5']

    if slot == "s1":
        card = usermarket[1]
        price = usermarket[2]
        p = "c1"
    if slot == "s2":
        card = usermarket[3]
        price = usermarket[4]
        p = "c2"
    if slot == "s3":
        card = usermarket[5]
        price = usermarket[6]
        p = "c3"
    if slot == "s4":
        card = usermarket[7]
        price = usermarket[8]
        p = "c4"
    if slot == "s5":
        card = usermarket[9]
        price = usermarket[10]
        p = "c5"
        
    if(str(slot) in str(slots)):
        if card == 0:
            await ctx.reply("nothing is selling in this slot")
        else:
            cursor.execute(f"UPDATE pmarket SET {str(slot)} = ? WHERE user_id = ?", (0, ctx.author.id))
            cursor.execute(f"UPDATE pmarket SET {str(p)} = ? WHERE user_id = ?", (0, ctx.author.id))
            await ctx.reply(f"🔶Your card `{card}` selling for {price}:coin: has been discarded from slot `{slot}`")
            db.commit()
        
    else:
        await ctx.reply("invalid slot number")


@client.command()
async def sales(ctx, card):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM pmarket")
    usermarket = cursor.fetchall()
    i = 0
    userlist = [] #users that are selling said card
    while i != len(usermarket)-1:
        tempuser = usermarket[i]
        if str(tempuser[1]) == str(card):
            userlist.append(f"<@{tempuser[0]}> -- {tempuser[2]}:coin: for `{card}`")
        if tempuser[3] == str(card):
            userlist.append(f"<@{tempuser[0]}> -- {tempuser[4]}:coin: for `{card}`")
        if tempuser[5] == str(card):
            userlist.append(f"<@{tempuser[0]}> -- {tempuser[6]}:coin: for `{card}`")
        if tempuser[7] == str(card):
            userlist.append(f"<@{tempuser[0]}> -- {tempuser[8]}:coin: for `{card}`")
        if tempuser[9] == str(card):
            userlist.append(f"<@{tempuser[0]}> -- {tempuser[10]}:coin: for `{card}`")
        i = i + 1
        print(i)
        print(len(usermarket))

    if i == len(usermarket)-1:
        
        embed = discord.Embed(title=f"`Card Sales`", description=f"shows sales of mentioned cards", color=discord.Color.teal())
        val = str(userlist)

        nval = val.replace(",","\n")
        n2val = nval.replace("[","")
        n3val = n2val.replace("]","")
        n4val = n3val.replace("'","")
        if len(userlist) == 0:
            embed.add_field(name=f"sales of `{card}`",value="no sales for this card")

        else:
            embed.add_field(name=f"sales of `{card}`",value=n4val)

        await ctx.send(embed= embed)

#rarityyy
@client.command()
async def rarity(ctx, card):
    db = sqlite3.connect("real.sqlite")
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM toty WHERE user_id = {ctx.author.id}")
    ownedcards = cursor.fetchone()
    cursor.execute(f"SELECT * FROM toty")
    allcards = cursor.fetchall()
    i = 0
    n = 0
    check = await ownershipcheck(card, ctx.author.id)
    if check == True:
        
        while i != len(allcards)-1:
            if(str(card) in str(allcards[i])):
                
                n = n + 1
            print(allcards[i])
            i = i + 1
        await ctx.reply(f"The card `{card}` is one in `{n}`")
    else:
        await ctx.reply("you do not have that card")

        
        
        


    




token = "hi"

# removed token for security
client.run(token)
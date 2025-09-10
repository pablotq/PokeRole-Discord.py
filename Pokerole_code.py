# BOT CODE -- For  easy use in python-based discord bots
# Keep in mind you'll need the .csv files in the same location as the bot
# --------------------------Fresh Setup---------------------------------------------

import csv
import math
import random
import discord
from discord.ext import commands


# -put your bot's discord token here
token = ''
# -what prefix you want to use to call the bot
prefix = '!'
bot = commands.Bot(command_prefix=prefix)


#
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# --next line goes at the very bottom
# bot.run(token)
#
#######

# ---------------------------Natures---------------------------
natures = dict()
stars = [0, 0, 0, 0, 0]


async def instantiateNatureList():
    with open('natures.csv', 'r', newline='', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            natures.update({row[0]: [row[1]] + row[2:]})


# ---------------------------Items---------------------------
pkmnItems = dict()


async def instantiateItemList():
    with open('PokeRoleItems.csv', 'r', encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            pkmnItems.update({row[0]: [row[1], row[13]]})
        pkmnItems.pop('Name')


async def pkmnitemhelper(item):
    if len(pkmnItems.keys()) == 0:
        await instantiateItemList()
    return pkmnItems[item.title()]


@bot.command(name='item', help='List an item\'s traits')
async def item_search(ctx, *, item_name):
    try:
        found = await pkmnitemhelper(item_name.strip().title())

        output = f'__{item_name.title()}__\n'
        if found[1] != '':
            output += f'**Pokemon**: {", ".join(found[1])}\n'
        output += f'**Description**: {found[0].capitalize()}'

        await ctx.send(output)
    except:
        await ctx.send(f'{item_name} wasn\'t found in the item list.')


# ---------------------------Abilities---------------------------
pkmnAbilities = dict()


async def instantiateAbilityList():
    with open('PokeRoleAbilities.csv', 'r', encoding="UTF-8") as file:
        reader = csv.reader(file)
        for row in reader:
            pkmnAbilities.update({row[0]: row[1:]})


@bot.command(name='ability', help='List an ability\'s traits')
async def item_search(ctx, *, ability):
    if len(pkmnItems.keys()) == 0:
        await instantiateAbilityList()
    try:
        found = pkmnAbilities[ability.title()]

        output = f'**__{ability.title()}:__**\n'
        output += f'- {found[0]}'

        await ctx.send(output)
    except:
        await ctx.send(f'{ability.title()} wasn\'t found in the ability list.')


# ---------------------------Moves---------------------------
pkmnMoves = dict()


async def instantiatePkmnMoveList():
    with open('pokeMoveSorted.csv', 'r', newline='', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            pkmnMoves.update({row[0]: row[1:]})


@bot.command(name='move', help='Lista o golpe')
async def move_search(ctx, *, term):
    if len(pkmnMoves.keys()) == 0:
        await instantiatePkmnMoveList()
    try:
        found = pkmnMoves[term.title()]

        output = f'__{term.title()}__\n'
        output += f'**Type**: {found[0].capitalize()}'
        output += f' -- **{found[1].capitalize()}**\n'
        output += f'**Target**: {found[7]}'
        output += f' -- **Power**: {found[2]}\n'
        output += f'**Dmg Mods**: {(found[3] or "None")} + {(found[4] or "None")}\n'
        output += f'**Acc Mods**: {(found[5] or "None")} + {(found[6] or "None")}\n'
        output += f'**Effect**: {found[8]}'

        await ctx.send(output)
    except:
        await ctx.send(f'{term} wasn\'t found in the move list.')


# ---------------------------Stats---------------------------
pkmnStats = dict()


async def instantiatePkmnStatList():
    with open('PokeroleRandom.csv', 'r', newline='', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            pkmnStats.update({row[1]: [row[0]] + row[2:]})


@bot.command(name='stats', help='List a pokemon\'s stats')
async def pkmn_search(ctx, *, term):
    if len(pkmnStats.keys()) == 0:
        await instantiatePkmnStatList()
    try:
        found = pkmnStats[term.title()]

        output = f'{found[0]} __{term.title()}__\n'
        output += f'**Generation**: {found[1]}\n'
        output += f'**Rank**: {found[21]}\n'
        output += f'**Type**: {found[2].capitalize()}'
        if found[3] == '':
            output += '\n'
        else:
            output += f' / {found[3].capitalize()}\n'
        output += f'**Base HP**: {found[4]}\n'
        output += f'**Strength**: {found[5]} ({found[10]})\n'
        output += f'**Dexterity**: {found[6]} ({found[11]})\n'
        output += f'**Vitality**: {found[7]} ({found[12]})\n'
        output += f'**Special**: {found[8]} ({found[13]})\n'
        output += f'**Insight**: {found[9]} ({found[14]})\n'
        output += f'**Defence**: 0 ({found[15]})\n'
        output += f'**Ability**: {found[16]}'
        if found[17] != '':  # secondary
            output += f' / {found[17]}'
        if found[18] != '':  # hidden
            output += f' ({found[18]})'
        output += '\n'
        output += f'**Can Evolve**: {(found[19] or "No")}\n'
        output += f'**Other Forms**: {(found[20] or "No")}\n'

        await ctx.send(output)
    except:
        await ctx.send(f'{term} wasn\'t found in the pokemon list.')


# ---------------------------Learn---------------------------
pkmnLearns = dict()


async def instantiatePkmnLearnsList():
    with open('PokeLearnMovesFull.csv', 'r', newline='', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            pkmnLearns.update({row[0][4:]: row[1:]})

@bot.command(name='d6', help='rola um d6')
async def d6(ctx):
    await ctx.send(random.randint(1,6))

@bot.command(name='pkmnlearns', help='Golpes q o pokemon aprende')
async def learn_search(ctx, *, term):
    if len(pkmnLearns.keys()) == 0:
        await instantiatePkmnLearnsList()
    try:
        found = pkmnLearns[term.title()]

        output = f'__{term.title()}__\n'
        moves = dict()
        for x in range(0, len(found), 2):
            if found[x + 1] not in moves:
                moves[found[x + 1]] = [found[x]]
            else:
                moves[found[x + 1]].append(found[x])

        for x in moves.keys():
            output += f'**{x}**\n' + '  |  '.join(moves[x]) + '\n'

        await ctx.send(output)
    except:
        await ctx.send(f'{term.title()} wasn\'t found in the pokeLearns list.')


# ---------------------------biomes---------------------------

pkmnBiomes = dict()


async def instantiatepkmnBiomesList():
    with open('habitats.csv', 'r', newline='', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if "Biomes" in row[0]:
                pkmnBiomes.update({row[0]: row[1:]})


@bot.command(name='biomes', help='Lists os biomes')
async def biome_search(ctx):
    if len(pkmnBiomes.keys()) == 0:
        await instantiatepkmnBiomesList()
    try:
        output = '**Biomes List:**\n'

        for x in pkmnBiomes.keys():
            output += f'- {x}\n'

        await ctx.send(output)
    except:
        await ctx.send(f'Couldn\'t list the biomes.')


@bot.command(name='habitats', help='Lista os habitas do bioma')
async def habitat_search(ctx, *, term=None):
    if len(pkmnBiomes.keys()) == 0:
        await instantiatepkmnHabitatsList()
    if len(pkmnBiomes.keys()) == 0:
        await instantiatepkmnBiomesList()
    try:

        if term is not None:
            output = f'**{term.title()} Habitats**\n'
            term += ' Biomes'
            found = pkmnBiomes[term.title()]
            for x in found:
                print(x)
                if x != '':
                    output += f'- {x}\n'
        else:
            found = pkmnHabitats
            output = f'**All Habitats**\n'
            for x in found.keys():
                if x != '':
                    output += f'- {x}\n'
            output += f'\n __É possível especificar o bioma e ver o habitats dele__'

        await ctx.send(output)
    except:
        await ctx.send(f'Couldn\'t list the habitats.')


# ---------------------------habitats---------------------------
pkmnHabitats = dict()


async def instantiatepkmnHabitatsList():
    with open('habitats.csv', 'r', newline='', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            if "Biomes" not in row[0]:
                pkmnHabitats.update({row[0]: row[1:]})



@bot.command(name='pkmn', help='Todos pokemons do habitat')
async def habitat_search(ctx, *, term):
    if len(pkmnHabitats.keys()) == 0:
        await instantiatepkmnHabitatsList()
    try:
        found = pkmnHabitats[term.title()]

        output = f'**Pokemons in {term.title()} :**\n'
        for x in found:
            if x != '':
                output += f'- {x}\n'

        await ctx.send(output)
    except:
        await ctx.send(f'Couldn\'t list the pokemons.')


@bot.command(name='onde', help='Habitats do pokemon')
async def random_search(ctx, *, term):
    if len(pkmnRand.keys()) == 0:
        await instantiatePkmnRandList()
    if len(pkmnHabitats.keys()) == 0:
        await instantiatepkmnHabitatsList()
    try:
        term = term.title()
        output = f'**{term}** Locations: \n'
        for key in pkmnHabitats:
            habitat = pkmnHabitats[key]
            for i in range(len(habitat)):
                if habitat[i] == term:
                    output += f'{key} / '

        await ctx.send(output)

    except:
        await ctx.send(f' couldn\'t pick a random pokemon.')


# ---------------------------RANDOM---------------------------
pkmnRand = dict()


async def instantiatePkmnRandList():
    with open('PokeroleRandom.csv', 'r', newline='', encoding="UTF-8") as infile:
        reader = csv.reader(infile)
        for row in reader:
            pkmnRand.update({row[1]: [row[0]] + row[2:]})


@bot.command(name='w', help='Gera pokemon escondido')
async def random_generate(ctx, pkmn, rank=None, style=None, shiny=None):

    member = ctx.author
    print(ctx.author)
    channel = await member.create_dm()

    if len(pkmnRand.keys()) == 0:
        await instantiatePkmnRandList()
    try:
        randPkmn = pkmnRand[pkmn.title()]
        if rank is None:
            rank = randPkmn[21]
        elif rank == 'balanced' or rank == 'fight' or rank == 'social':
            style = rank
            rank = randPkmn[21]
        rank = rank.title()
        if style is None:
            styles = ['fight', 'balanced', 'social']
            s = random.choices(styles, weights=(20, 70, 10), k=1)
            style = s[0]

        if shiny is None:
            if rank.title() == 'Shiny':
                shiny = 1
                rank = randPkmn[21]
            elif style.title() == 'Shiny':
                shiny = 1
                styles = ['fight', 'balanced', 'social']
                s = random.choices(styles, weights=(20, 70, 10), k=1)
                style = s[0]
            else:
                shiny = random.randint(1, 500)
        elif shiny.title() == 'Shiny':
            shiny = 1

        ditto = random.randint(1, 750)
        output = await set_stats(randPkmn, pkmn.title(), rank, style, ditto, shiny, ctx)

        #await ctx.send(output)
        await channel.send(output)

    except:
        await ctx.send(f'**{pkmn.title()}** wasn\'t found in the pokemon list.')


@bot.command(name='gen', help='Gera pokemon')
async def random_generate(ctx, pkmn, rank=None, style=None, shiny=None):

    member = ctx.author
    print(ctx.author)
    channel = await member.create_dm()

    if len(pkmnRand.keys()) == 0:
        await instantiatePkmnRandList()
    try:
        randPkmn = pkmnRand[pkmn.title()]
        if rank is None:
            rank = randPkmn[21]
        elif rank == 'balanced' or rank == 'fight' or rank == 'social':
            style = rank
            rank = randPkmn[21]
        rank = rank.title()
        if style is None:
            styles = ['fight', 'balanced', 'social']
            s = random.choices(styles, weights=(20, 70, 10), k=1)
            style = s[0]

        if shiny is None:
            if rank.title() == 'Shiny':
                shiny = 1
                rank = randPkmn[21]
            elif style.title() == 'Shiny':
                shiny = 1
                styles = ['fight', 'balanced', 'social']
                s = random.choices(styles, weights=(20, 70, 10), k=1)
                style = s[0]
            else:
                shiny = random.randint(1, 500)
        elif shiny.title() == 'Shiny':
            shiny = 1

        ditto = random.randint(1, 750)
        output = await set_stats(randPkmn, pkmn.title(), rank, style, ditto, shiny, ctx)

        await ctx.send(output)
        #await channel.send(output)

    except:
        await ctx.send(f'**{pkmn.title()}** wasn\'t found in the pokemon list.')


@bot.command(name='rp', help='Get a random pokemon')
async def rp_search(ctx, num='1', rank_min='Starter', rank_max=None, gen=0):

    member = ctx.author
    channel = await member.create_dm()

    if len(pkmnHabitats.keys()) == 0:
        await instantiatepkmnHabitatsList()
    try:
        pkmnList = []
        pkmnList.append('Capybraba')
        pkmnList.append('Capyba')
        for i in pkmnHabitats.keys():
            for k in pkmnHabitats[i]:
                if k != '':
                    pkmnList.append(k)
        pkmnList.append('Capybraba')
        pkmnList.append('Capyba')
        print(pkmnHabitats)
        print(pkmnList)
        try:
            time = int(num)
            if rank_max is None:
                rank_max = rank_min
                rank_min = 'Starter'
        except:
            time = 1
            if rank_min != 'Starter':
                rank_max = rank_min
                rank_min = num
            else:
                rank_max = num

        output = False
        count = 0
        check = 0
        final = ''
        while not output:
            count += 1
            randPkmn = ''
            while randPkmn == '':
                randPkmn = random.choice(pkmnList)
            print(f'get_pokemon({randPkmn.title()}, {rank_min.title()}, {rank_max.title()}, {gen})')
            output = await get_pokemon(randPkmn.title(), rank_min.title(), rank_max.title(), gen)
            if output:
                check += 1
                final += output
                if check < time:
                    output = False

            if count >= 100000:
                final = f'Couldn\'t find a random pokemon between ranks **{rank_min.title()}** and **{rank_max.title()}**.'
                break

        await channel.send(final)
        #await ctx.send(final)

    except:
        await ctx.send(f'Couldn\'t get a random pokemon from the habitat.')

@bot.command(name='rph', help='Get a random pokemon from the habitat')
async def rph_search(ctx, term, num='1', rank_min='Starter', rank_max=None, gen=0):

    member = ctx.author
    print(ctx.author)
    channel = await member.create_dm()

    if len(pkmnHabitats.keys()) == 0:
        await instantiatepkmnHabitatsList()
    try:
        pkmnList = []
        pkmnList.append('Capybraba')
        pkmnList.append('Capyba')
        for k in pkmnHabitats[term.title()]:
            if k != '':
                pkmnList.append(k)
        pkmnList.append('Capybraba')
        pkmnList.append('Capyba')
        try:
            time = int(num)
            if rank_max is None:
                rank_max = rank_min
                rank_min = 'Starter'
        except:
            time = 1
            if rank_min != 'Starter':
                rank_max = rank_min
                rank_min = num
            else:
                rank_max = num

        output = False
        count = 0
        check = 0
        final = ''
        while not output:
            count += 1
            randPkmn = ''
            while randPkmn == '':
                randPkmn = random.choice(pkmnList)
            print(f'get_pokemon({randPkmn.title()}, {rank_min.title()}, {rank_max.title()}, {gen})')
            output = await get_pokemon(randPkmn.title(), rank_min.title(), rank_max.title(), gen)
            if output:
                check += 1
                final += output
                if check < time:
                    output = False

            if count >= 100000:
                final = f'Couldn\'t find a random pokemon between ranks **{rank_min.title()}** and **{rank_max.title()}**.'
                break

        await channel.send(final)
        #await ctx.send(final)

    except:
        await ctx.send(f'Couldn\'t get a random pokemon from the habitat.')


@bot.command(name='rpb', help='Get a random pokemon from the biome')
async def rpb_search(ctx, term, num='1', rank_min='Starter', rank_max=None, gen=0):

    member = ctx.author
    print(ctx.author)
    channel = await member.create_dm()

    term += " Biomes"

    if len(pkmnBiomes.keys()) == 0:
        await instantiatepkmnBiomesList()
    if len(pkmnHabitats.keys()) == 0:
        await instantiatepkmnHabitatsList()
    try:
        biome = pkmnBiomes[term.title()]
        try:
            time = int(num)
            if rank_max is None:
                rank_max = rank_min
                rank_min = 'Starter'
        except:
            time = 1
            if rank_min != 'Starter':
                rank_max = rank_min
                rank_min = num
            else:
                rank_max = num

        output = False
        count1 = 0
        check = 0
        final = ''
        pokemon_list = []
        pokemon_list.append('Capybraba')
        pokemon_list.append('Capyba')

        for i in biome:
            if i != '':
                for k in pkmnHabitats[i]:
                    if k != '':
                        pokemon_list.append(k)

        pokemon_list.append('Capybraba')
        pokemon_list.append('Capyba')

        while not output:
            count1 += 1
            randPkmn = random.choice(pokemon_list)

            print(f'get_pokemon({randPkmn.title()}, {rank_min.title()}, {rank_max.title()}, {gen})')
            output = await get_pokemon(randPkmn.title(), rank_min.title(), rank_max.title(), gen)
            if output:
                check += 1
                final += output
                if check < time:
                    output = False

            if count1 >= 100000:
                final = f'Couldn\'t find a random pokemon between ranks **{rank_min.title()}** and **{rank_max.title()}**.'
                break
        print(f'iterações: {count1}')
        print(pokemon_list)
        #--await channel.send(final)
        await ctx.send(final)
    except:
        await ctx.send(f'Couldn\'t list the habitats.')


# ---------------------------get stats---------------------------

async def get_stats(pkmn):
    if len(pkmnRand.keys()) == 0:
        await instantiatePkmnRandList()
    try:
        found = pkmnRand[pkmn]

        output = f'{found[0]} __{pkmn}__\n'
        output += f'**Rank**: {found[20]}\n'
        output += f'**Type**: {found[1].capitalize()}'
        if found[2] == '':
            output += '\n'
        else:
            output += f' / {found[2].capitalize()}\n'
        output += f'**Base HP**: {found[3]}\n'
        output += f'**Strength**: {found[4]} ({found[5]})\n'
        output += f'**Dexterity**: {found[6]} ({found[7]})\n'
        output += f'**Vitality**: {found[8]} ({found[9]})\n'
        output += f'**Special**: {found[10]} ({found[11]})\n'
        output += f'**Insight**: {found[12]} ({found[13]})\n'
        output += f'**Ability**: {found[14]}'
        if found[15] != '':  # secondary
            output += f' / {found[15]}'
        if found[16] != '':  # hidden
            output += f' ({found[16]})'
        if found[17] != '':  # event
            output += f' <{found[17]}>'
        output += '\n'
        output += f'**Can Evolve**: {(found[18] or "No")}\n'
        output += f'**Other Forms**: {(found[19] or "No")}\n'

        return output
    except:
        return f'**{pkmn.capitalize()}** wasn\'t found in the pokemon list.'


# ---------------------------get pokemon---------------------------

async def get_pokemon(pkmn, rank_min, rank_max, gen):
    if len(pkmnRand.keys()) == 0:
        await instantiatePkmnRandList()
    try:
        if pkmn == 'Wormadam':
            wormadam = ['Grass', 'Steel', 'Ground']
            pkmn += f' {random.choice(wormadam)}'

        if pkmn == 'Oricorio':
            oricorio = ['Baile', 'Pom-Pom', 'Pa\'u', 'Sensu', 'Samba']
            pkmn += f' {random.choice(oricorio)}'

        found = pkmnRand[pkmn]
        ranks = {'Starter': 1, 'Beginner': 2, 'Amateur': 3, 'Ace': 4, 'Pro': 5}
        check1 = ranks[rank_min]
        check2 = ranks[rank_max]
        pkmn_rank = ranks[found[21]]
        print(f'{check2} >= {pkmn_rank} >= {check1}')
        print(f'if {gen} == 0 or {gen} == {int(found[1])}:')
        if gen == 0 or gen == int(found[1]):
            print('gen ok')
            if check2 >= pkmn_rank >= check1:
                # print('if ok')
                output = f'- __{pkmn}__ '
                output += f'**Rank**: {found[21]}\n'
                print(gen)

                return output
            else:
                return False
        else:
            return False

    except:
        return f'**{pkmn}** wasn\'t found in the pokemon list.\n'


# ---------------------------ping---------------------------

@bot.command(name='ping', help='Test if bot is ok')
async def ping(ctx):
    await ctx.send("pong!")


# ---------------------------random attributes---------------------------

async def gen_attr(pkmn, style, shiny, rank, ctx):
    found = pkmn
    rank1 = random.randint(1, 100)
    rank2 = random.randint(1, 100)
    rank3 = random.randint(1, 100)
    total = 0
    total_attr = 0
    total_social = 0
    attributes = []

    try:
        for i in range(len(stars)):
            stars[i] = 0

        if rank == 'Starter':
            total += 4
            stars[0] = 1
        elif rank == 'Beginner':
            total += 4
            stars[0] = 1
            print('1 - Starter ok')
            if rank1 <= 70:
                total += 4
                stars[1] = 1
                print('2 - Beginner ok')
        elif rank == 'Amateur':
            total += 4
            stars[0] = 1
            print('1 - Starter ok')
            if rank1 <= 80:
                total += 4
                stars[1] = 1
                print('2 - Beginner ok')
            if rank2 <= 60:
                total += 4
                stars[2] = 1
                print('3 - Amateur ok')
        elif rank == 'Ace':
            total += 4
            stars[0] = 1
            print('1 - Starter ok')
            if rank1 <= 80:
                total += 4
                stars[1] = 1
                print('2 - Beginner ok')
            if rank2 <= 60:
                total += 4
                stars[2] = 1
                print('3 - Amateur ok')
            if rank3 <= 40:
                total += 4
                stars[3] = 1
                print('4 - Ace ok')
        elif rank == 'Pro':
            total += 8
            stars[0] = 1
            stars[1] = 1
            print('1 - Starter ok')
            print('2 - Beginner ok')
            if rank1 <= 80:
                total += 4
                stars[2] = 1
                print('3 - Amateur ok')
            if rank2 <= 60:
                total += 4
                stars[3] = 1
                print('4 - Ace ok')
            if rank3 <= 40:
                total += 6
                stars[4] = 1
                print('5 - Pro ok')

        if style == 'fight':
            # total_attr = total + int(found[22]) - 5
            total_attr = int(math.ceil(total * 0.80))
            total_social = int(math.floor(total * 0.20)) + 1
        elif style == 'balanced':
            total_attr = int(total / 2)
            total_social = int(total / 2) + 1
        elif style == 'social':
            # total_attr = int(found[22]) - 5
            total_attr = int(math.floor(total * 0.20))
            total_social = int(math.ceil(total * 0.80)) + 1

        print('style ok')
        if shiny == 1:
            limit = [int(found[10]) + 1, int(found[11]) + 1, int(found[12]) + 1, int(found[13]) + 1, int(found[14]) + 1,
                     int(found[15]) + 1]

            social = [2, 2, 2, 2, 2]
            limit_social = 6
        else:
            limit = [found[10], found[11], found[12], found[13], found[14], found[15]]

            social = [1, 1, 1, 1, 1]
            limit_social = 5

        print('limits ok')
        r = random.randint(1, 2)
        type = found[2]
        if type == 'Normal':
            if r == 1:
                print('Up vitality')
                if shiny == 1:  # vitality
                    attributes = [2, 2, 3, 2, 2, 2]
                else:
                    attributes = [1, 1, 2, 1, 1, 1]
            else:
                print('Up dexterity')
                if shiny == 1:  # dexterity
                    attributes = [2, 3, 2, 2, 2, 2]
                else:
                    attributes = [1, 2, 1, 1, 1, 1]
        elif type == 'Fire':
            if r == 1:
                print('Up special')
                if shiny == 1:  # special
                    attributes = [2, 2, 2, 3, 2, 2]
                else:
                    attributes = [1, 1, 1, 2, 1, 1]
            else:
                print('Up dexterity')
                if shiny == 1:  # dexterity
                    attributes = [2, 3, 2, 2, 2, 2]
                else:
                    attributes = [1, 2, 1, 1, 1, 1]
        elif type == 'Water':
            if r == 1:
                print('Up vitality')
                if shiny == 1:  # vitality
                    attributes = [2, 2, 3, 2, 2, 2]
                else:
                    attributes = [1, 1, 2, 1, 1, 1]
            else:
                print('Up defense')
                if shiny == 1:  # defense
                    attributes = [2, 2, 2, 2, 2, 3]
                else:
                    attributes = [1, 1, 1, 1, 1, 2]
        elif type == 'Electric':
            if r == 1:
                print('Up dexterity')
                if shiny == 1:  # dexterity
                    attributes = [2, 3, 2, 2, 2, 2]
                else:
                    attributes = [1, 2, 1, 1, 1, 2]
            else:
                print('Up special')
                if shiny == 1:  # special
                    attributes = [2, 2, 2, 3, 2, 2]
                else:
                    attributes = [1, 1, 1, 2, 1, 1]
        elif type == 'Grass':
            if r == 1:
                print('Up defense')
                if shiny == 1:  # defense
                    attributes = [2, 2, 2, 2, 2, 3]
                else:
                    attributes = [1, 1, 1, 1, 1, 2]
            else:
                print('Up special')
                if shiny == 1:  # special
                    attributes = [2, 2, 2, 3, 2, 2]
                else:
                    attributes = [1, 1, 1, 2, 1, 1]
        elif type == 'Ice':
            if r == 1:
                print('Up vitality')
                if shiny == 1:  # vitality
                    attributes = [2, 2, 3, 2, 2, 2]
                else:
                    attributes = [1, 1, 2, 1, 1, 1]
            else:
                print('Up special')
                if shiny == 1:  # special
                    attributes = [2, 2, 2, 3, 2, 2]
                else:
                    attributes = [1, 1, 1, 2, 1, 1]
        elif type == 'Fighting':
            if r == 1:
                print('Up vitality')
                if shiny == 1:  # vitality
                    attributes = [2, 2, 3, 2, 2, 2]
                else:
                    attributes = [1, 1, 2, 1, 1, 1]
            else:
                print('Up strength')
                if shiny == 1:  # strength
                    attributes = [3, 2, 2, 2, 2, 2]
                else:
                    attributes = [2, 1, 1, 1, 1, 1]
        elif type == 'Poison':
            if r == 1:
                print('Up dexterity')
                if shiny == 1:  # dexterity
                    attributes = [2, 3, 2, 2, 2, 2]
                else:
                    attributes = [1, 2, 1, 1, 1, 1]
            else:
                print('Up special')
                if shiny == 1:  # special
                    attributes = [2, 2, 2, 3, 2, 2]
                else:
                    attributes = [1, 1, 1, 2, 1, 1]
        elif type == 'Ground':
            if r == 1:
                print('Up defense')
                if shiny == 1:  # defense
                    attributes = [2, 2, 2, 2, 2, 3]
                else:
                    attributes = [1, 1, 1, 1, 1, 2]
            else:
                print('Up vitality')
                if shiny == 1:  # vitality
                    attributes = [2, 2, 3, 2, 2, 2]
                else:
                    attributes = [1, 1, 2, 1, 1, 1]
        elif type == 'Flying':
            if r == 1:
                print('Up dexterity')
                if shiny == 1:  # dexterity
                    attributes = [2, 3, 2, 2, 2, 2]
                else:
                    attributes = [1, 2, 1, 1, 1, 1]
            else:
                print('Up special')
                if shiny == 1:  # special
                    attributes = [2, 2, 2, 3, 2, 2]
                else:
                    attributes = [1, 1, 1, 2, 1, 1]
        elif type == 'Psychic':
            if r == 1:
                print('Up insight')
                if shiny == 1:  # insight
                    attributes = [2, 2, 2, 2, 3, 2]
                else:
                    attributes = [1, 1, 1, 1, 2, 1]
            else:
                print('Up special')
                if shiny == 1:  # special
                    attributes = [2, 2, 2, 3, 2, 2]
                else:
                    attributes = [1, 1, 1, 2, 1, 1]
        elif type == 'Bug':
            if r == 1:
                print('Up defense')
                if shiny == 1:  # defense
                    attributes = [2, 2, 2, 2, 2, 3]
                else:
                    attributes = [1, 1, 1, 1, 1, 2]
            else:
                print('Up dexterity')
                if shiny == 1:  # dexterity
                    attributes = [2, 3, 2, 2, 2, 2]
                else:
                    attributes = [1, 2, 1, 1, 1, 1]
        elif type == 'Rock':
            if r == 1:
                print('Up defense')
                if shiny == 1:  # defense
                    attributes = [2, 2, 2, 2, 2, 3]
                else:
                    attributes = [1, 1, 1, 1, 1, 2]
            else:
                print('Up strength')
                if shiny == 1:  # strength
                    attributes = [3, 2, 2, 2, 2, 2]
                else:
                    attributes = [2, 1, 1, 1, 1, 1]
        elif type == 'Ghost':
            if r == 1:
                print('Up defense')
                if shiny == 1:  # defense
                    attributes = [2, 2, 2, 2, 2, 3]
                else:
                    attributes = [1, 1, 1, 1, 1, 2]
            else:
                print('Up insight')
                if shiny == 1:  # insight
                    attributes = [2, 2, 2, 2, 3, 2]
                else:
                    attributes = [1, 1, 1, 1, 2, 1]
        elif type == 'Dragon':
            if r == 1:
                print('Up vitality')
                if shiny == 1:  # vitality
                    attributes = [2, 2, 3, 2, 2, 2]
                else:
                    attributes = [1, 1, 2, 1, 1, 1]
            else:
                print('Up strength')
                if shiny == 1:  # strength
                    attributes = [3, 2, 2, 2, 2, 2]
                else:
                    attributes = [2, 1, 1, 1, 1, 1]
        elif type == 'Dark':
            if r == 1:
                print('Up strength')
                if shiny == 1:  # strength
                    attributes = [3, 2, 2, 2, 2, 2]
                else:
                    attributes = [2, 1, 1, 1, 1, 1]
            else:
                print('Up dexterity')
                if shiny == 1:  # dexterity
                    attributes = [2, 3, 2, 2, 2, 2]
                else:
                    attributes = [1, 2, 1, 1, 1, 1]
        elif type == 'Steel':
            if r == 1:
                print('Up defense')
                if shiny == 1:  # defense
                    attributes = [2, 2, 2, 2, 2, 3]
                else:
                    attributes = [1, 1, 1, 1, 1, 2]
            else:
                print('Up insight')
                if shiny == 1:  # insight
                    attributes = [2, 2, 2, 2, 3, 2]
                else:
                    attributes = [1, 1, 1, 1, 2, 1]
        elif type == 'Fairy':
            if r == 1:
                print('Up insight')
                if shiny == 1:  # insight
                    attributes = [2, 2, 2, 2, 3, 2]
                else:
                    attributes = [1, 1, 1, 1, 2, 1]
            else:
                print('Up vitality')
                if shiny == 1:  # vitality
                    attributes = [2, 2, 3, 2, 2, 2]
                else:
                    attributes = [1, 1, 2, 1, 1, 1]

        for k in range(500):
            sort1 = 1  # random.randint(1, 2)
            if sort1 < total_attr:
                if sort1 != 0:
                    i = random.randint(0, 5)
                    if attributes[i] + sort1 <= int(limit[i]):
                        attributes[i] += sort1
                        total_attr -= sort1
        print('attributes ok')

        for k in range(500):
            sort = random.randint(1, 2)
            if sort < total_social:
                if sort != 0:
                    i = random.randint(0, 4)
                    if social[i] + sort <= limit_social:
                        social[i] += sort
                        total_social -= sort
        print('social ok')

        final = attributes + social
        return final
    except:
        await ctx.send(f'Couldn\'t generate random attributes.')



# ---------------------------random skills---------------------------

async def gen_skill(rank, style, ctx):
    skills = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sum = 0
    limit = 0

    try:
        if rank.capitalize() == 'Starter':
            sum = 3
            limit = 1
        elif rank.capitalize() == 'Beginner':
            sum = 6
            limit = 2
        elif rank.capitalize() == 'Amateur':
            sum = 9
            limit = 3
        elif rank.capitalize() == 'Ace':
            sum = 13
            limit = 4
        elif rank.capitalize() == 'Pro':
            sum = 16
            limit = 5
        elif rank.capitalize() == 'Master':
            sum = 16
            limit = 7
            skills = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

        total = sum
        position = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        r = []

        for k in range(500):
            sort = math.floor(random.random() * total)
            if sort < total:
                if sort != 0:
                    if style == 'fight':
                        r = random.choices(position, weights=(12, 12, 12, 12, 9, 9, 9, 9, 6, 2, 6, 2), k=1)
                    elif style == 'social':
                        r = random.choices(position, weights=(2, 2, 2, 8, 10, 10, 10, 10, 11, 11, 11, 13), k=1)
                    elif style == 'balanced':
                        r = random.choices(position, k=1)
                    i = int(r[0])
                    if skills[i] + sort <= limit:
                        skills[i] += sort
                        total -= sort

        return skills
    except:
        await ctx.send(f'Couldn\'t generate random skills.')


# ---------------------------random moves---------------------------
async def gen_move(pkmn, rank, num, ctx):
    count = int(num)

    try:
        if count > 4:
            count = 4
        if len(pkmnLearns.keys()) == 0:
            await instantiatePkmnLearnsList()

        found = pkmnLearns[pkmn.title()]

        moves = dict()
        movesList = []

        for x in range(0, len(found), 2):
            if found[x + 1] not in moves:
                moves[found[x + 1]] = [found[x]]
            else:
                moves[found[x + 1]].append(found[x])

        if rank.capitalize() == 'Starter':
            if 'Starter' in moves:
                movesList += moves['Starter']
        elif rank.capitalize() == 'Beginner':
            if 'Starter' in moves:
                movesList += moves['Starter']
            if 'Beginner' in moves:
                movesList += moves['Beginner']
        elif rank.capitalize() == 'Amateur':
            if 'Starter' in moves:
                movesList += moves['Starter']
            if 'Beginner' in moves:
                movesList += moves['Beginner']
            if 'Amateur' in moves:
                movesList += moves['Amateur']
        elif rank.capitalize() == 'Ace':
            if 'Starter' in moves:
                movesList += moves['Starter']
            if 'Beginner' in moves:
                movesList += moves['Beginner']
            if 'Amateur' in moves:
                movesList += moves['Amateur']
            if 'Ace' in moves:
                movesList += moves['Ace']
        elif rank.capitalize() == 'Pro':
            if 'Starter' in moves:
                movesList += moves['Starter']
            if 'Beginner' in moves:
                movesList += moves['Beginner']
            if 'Amateur' in moves:
                movesList += moves['Amateur']
            if 'Ace' in moves:
                movesList += moves['Ace']
            if 'Pro' in moves:
                movesList += moves['Pro']
            if 'Master' in moves:
                movesList += moves['Master']
        elif rank.capitalize() == 'Master':
            if 'Starter' in moves:
                movesList += moves['Starter']
            if 'Beginner' in moves:
                movesList += moves['Beginner']
            if 'Amateur' in moves:
                movesList += moves['Amateur']
            if 'Ace' in moves:
                movesList += moves['Ace']
            if 'Pro' in moves:
                movesList += moves['Pro']
            if 'Master' in moves:
                movesList += moves['Master']

        if count > len(movesList):
            count = len(movesList)
        randMoves = random.sample(movesList, k=count)

        return randMoves
    except:
        await ctx.send(f'Couldn\'t generate random moves.')


# ---------------------------generate stats---------------------------
async def set_stats(pkmn, name, rank, style, ditto, shiny, ctx):
    if len(natures.keys()) == 0:
        await instantiateNatureList()
    try:

        found = pkmn
        n = random.choice(list(natures.keys()))
        nature = natures[n]
        overgrowth = random.randint(1, 100)
        print(f'pokemon: {name} - {rank}')
        print(f'[{style}]')

        attr = await gen_attr(pkmn, style, shiny, rank, ctx)
        skills = await gen_skill(rank, style, ctx)
        print('skills ok')
        num = attr[4] + 2  # number of moves
        moves = await gen_move(name, rank, num, ctx)
        print('moves ok')
        abilities = [found[16], found[17], found[18]]
        hp = int(found[4]) + attr[2]
        if overgrowth <= 10:
            hp += 1

        output = f'**{found[0]} __{name}__** '
        if found[22] == '':
            gender = [':female_sign:', ':male_sign:']
            output += f'{random.choice(gender)} '
        else:
            if found[22] == 'F':
                output += ':female_sign: '
            elif found[22] == 'M':
                output += ':male_sign: '
            elif found[22] == 'N':
                output += ':regional_indicator_n: '

        if style == 'fight':
            output += ':martial_arts_uniform: '
        elif style == 'social':
            output += ':performing_arts: '

        print(stars)
        for i in range(len(stars)):
            if stars[i] == 1:
                output += ':star: '

        output += '\n'

        if shiny == 1:
            output += ' :sparkles:__**SHINY!**__:sparkles:\n'  # :sparkles:
        if ditto == 1:
            output += ' :purple_circle:__**DITTO!**__:purple_circle:\n'  # :purple_circle:
        # output += f'\n**Rank**: {found[20]}  '
        output += f'**Rank**: {rank}  '
        output += f'**Type**: {found[2].capitalize()}'
        if found[3] == '':
            output += '\n'
        else:
            output += f' / {found[3].capitalize()}\n'

        if abilities[1] == '' and abilities[2] == '':
            output += f'**Ability**: {abilities[0]}\n'
        elif abilities[1] == '':
            output += f'**Ability**: {random.choices(abilities, weights=(90, 0, 10), k=1)}'
        elif abilities[2] == '':
            output += f'**Ability**: {random.choices(abilities, weights=(50, 50, 0), k=1)}'
        else:
            output += f'**Ability**: {random.choices(abilities, weights=(45, 45, 10), k=1)}'

        output += f'\n**Nature**: {nature[0]}   **Confidence:** {nature[1]}'
        if overgrowth <= 10:
            output += f'\n**HP**: {hp}  (OVERGROWTH)\n'
        else:
            output += f'\n**HP**: {hp}\n'

        if shiny != 1:
            output += f'**Strength**: {attr[0]} ({found[10]})    '
            # output += f'**Tough**: {social[0]}\n'
            output += f'**Tough**: {attr[6]}\n'
            output += f'**Dexterity**: {attr[1]} ({found[11]})   '
            # output += f'**Beauty**: {social[1]}\n'
            output += f'**Beauty**: {attr[7]}\n'
            output += f'**Vitality**: {attr[2]} ({found[12]})        '
            # output += f'**Cool**: {social[2]}\n'
            output += f'**Cool**: {attr[8]}\n'
            output += f'**Special**: {attr[3]} ({found[13]})        '
            # output += f'**Cute**: {social[3]}\n'
            output += f'**Cute**: {attr[9]}\n'
            output += f'**Insight**: {attr[4]} ({found[14]})        '
            # output += f'**Clever**: {social[4]}\n'
            output += f'**Clever**: {attr[10]}\n'
            output += f'**Defence**: {attr[5]} ({found[15]})\n'
        else:
            output += f'**Strength**: {attr[0]} ({int(found[10]) + 1})    '
            # output += f'**Tough**: {social[0]}\n'
            output += f'**Tough**: {attr[6]}\n'
            output += f'**Dexterity**: {attr[1]} ({int(found[11]) + 1})   '
            # output += f'**Beauty**: {social[1]}\n'
            output += f'**Beauty**: {attr[7]}\n'
            output += f'**Vitality**: {attr[2]} ({int(found[12]) + 1})        '
            # output += f'**Cool**: {social[2]}\n'
            output += f'**Cool**: {attr[8]}\n'
            output += f'**Special**: {attr[3]} ({int(found[13]) + 1})        '
            # output += f'**Cute**: {social[3]}\n'
            output += f'**Cute**: {attr[9]}\n'
            output += f'**Insight**: {attr[4]} ({int(found[14]) + 1})        '
            # output += f'**Clever**: {social[4]}\n'
            output += f'**Clever**: {attr[10]}\n'
            output += f'**Defence**: {attr[5]} ({int(found[15] )+ 1}) \n'

        output += f'Total attr: {attr[0] + attr[1] + attr[2] + attr[3] + attr[4] + attr[5] - 5}    '
        # output += f'Total social: {social[0] + social[1] + social[2] + social[3] + social[4]}\n'
        output += f'Total social: {attr[6] + attr[7] + attr[8] + attr[9] + attr[10] - 5}\n'

        output += '__**Skills:**__\n'
        for k in range(len(skills)):
            if skills[k] != 0:
                if k == 0:
                    output += '**Brawl**: '
                    output += f'{skills[k]}       '
                elif k == 1:
                    output += '**Channel**: '
                    output += f'{skills[k]}       '
                elif k == 2:
                    output += '**Clash**: '
                    output += f'{skills[k]}      '
                elif k == 3:
                    output += '**Evasion**: '
                    output += f'{skills[k]}\n'
                elif k == 4:
                    output += '**Alert**: '
                    output += f'{skills[k]}      '
                elif k == 5:
                    output += '**Athletic**: '
                    output += f'{skills[k]}      '
                elif k == 6:
                    output += '**Nature**: '
                    output += f'{skills[k]}      '
                elif k == 7:
                    output += '**Stealth**: '
                    output += f'{skills[k]}\n'
                elif k == 8:
                    output += '**Allure**: '
                    output += f'{skills[k]}      '
                elif k == 9:
                    output += '**Etiquette**: '
                    output += f'{skills[k]}      '
                elif k == 10:
                    output += '**Intimidate**: '
                    output += f'{skills[k]}      '
                elif k == 11:
                    output += '**Perform**: '
                    output += f'{skills[k]}'

        output += f'\n**__Moves:__**\n'
        for x in range(len(moves)):
            output += f'__{moves[x]}__ / '

        return output
    except:
        return f'Couldn\'t set random stats for **{name}**.'


@bot.command(name='dm', pass_context=True)
async def send_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)
# ------------------------run bot-----------------------------------

bot.run(token)

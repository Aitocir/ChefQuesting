
import random
import Queue

from constants import *

def d20():
    return random.randrange(1,21)

def monster_for_tile(tile):
   adjs = ['fearsome', 'giant', 'terrifying', 'powerful', 'massive', 'monstrous']
   hasTree = tile & MASK_tree != 0
   hasBush = tile & MASK_bush != 0
   if hasTree:
      return random.choice(adjs) + ' bear'
   elif hasBush:
      return random.choice(adjs) + ' wolf'
   else:
      return random.choice(adjs) + ' snake'

def time_of_day(timestamp):
    if timestamp < 0:
        return 'armageddon'
    times = ['dawn', 'morning', 'noon', 'afternoon', 'dusk', 'evening', 'midnight', 'twilight']
    return times[timestamp % 8] + ' on Day ' + str((timestamp // 8) + 1)

def send_message_to_game(game, msg, connections, typeCode):
   for p in game[IDX_players]:
      q = connections[p][IDX_qOut]
      q.put(typeCode + msg)

def list_current_games(games, connections):
    output = ''
    for gameName in games:
        if gameName == 'Lobby':
            continue
        output += gameName
        spaces = []
        for i in range(40-len(gameName)):
            spaces += ' '
        output += ''.join(spaces)
        for p in games[gameName][IDX_players]:
            output += connections[p][IDX_name] + ', '
        output += '\n'
    if len(output) < 3:
        return ''
    else:
        return output[0:len(output)-3]

def advance_time(game):
    hb = game[IDX_hunger]
    game[IDX_time] += 1
    game[IDX_hunger] += 1
    ha = game[IDX_hunger]
    if ha >= 8 and (hb % 4) >= (ha % 4):
        game[IDX_alert] = True

def add_combat_hunger(game, caughtOffGuard):
    hb = game[IDX_hunger]
    game[IDX_hunger] += 2 if caughtOffGuard else 1
    ha = game[IDX_hunger]
    if ha >= 8 and (hb % 4) >= (ha % 4):
        game[IDX_alert] = True

def describe_hunger(hunger):
    if hunger < 4:
        return 'Everyone is still full from their last meal.'
    elif hunger < 8:
        return 'The party could go for a snack, perhaps.'
    elif hunger < 12:
        return 'The group is feeling pretty hungry.'
    elif hunger < 16:
        return 'The growling of stomaches provides a depressing undertones to the sounds of nature.'
    elif hunger < 20:
        return 'Questing is proving difficult while having hallucinations of fried chicken.'
    elif hunger < 24:
        return 'The cold embrace of death begins to sound preferable to this gnawing, never-ending hunger.'
    else:
        return 'You lay unconscious on the ground, about to die of hunger.'

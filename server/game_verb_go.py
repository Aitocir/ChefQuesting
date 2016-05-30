
import random

from combat import *
from constants import *
from game_utility import *

def game_verb_go_results(playerName, game, dir, connections):
   tileIdx = -1
   currentIdx = game[IDX_location]
   if dir == 'north':
      tileIdx = currentIdx - 16 if currentIdx - 16 > -1 else -2
   if dir == 'south':
      tileIdx = currentIdx + 16 if currentIdx + 16 < 256 else -2
   if dir == 'west':
      tileIdx = currentIdx - 1 if currentIdx % 16 != 0 else -2
   if dir == 'east':
      tileIdx = currentIdx + 1 if currentIdx % 16 != 15 else -2
   message = playerName + ' '
   if tileIdx == -2:
      message += 'boldly strides ' + dir + 'ward, only to notice the sudden drop off into oblivion and decide to stay put.'
   elif tileIdx == -1:
      message += 'tries leading everyone \"' + dir + '\" confidently, but fails because this is not a fairy tale, and that is not a real direction.'
   else:
      #  go is going to happen for real, change players' location and start fight if necessary
      game[IDX_location] = tileIdx
      advance_time(game)
      message += 'and entourage journey ' + dir + 'ward until ' + time_of_day(game[IDX_time])
      isMonster = game[IDX_map][tileIdx] & MASK_monster != 0
      newHere = game[IDX_map][tileIdx] & MASK_visited == 0
      sawItComin = game[IDX_map][tileIdx] & MASK_opinion != 0
      game[IDX_map][tileIdx] = game[IDX_map][tileIdx] | MASK_visited
      if not isMonster:
         message += ', free of incident.'
      elif not newHere:
         message += ', and to the surprise of no one, the ' + monster_for_tile(game[IDX_map][tileIdx]) + ' is still here waiting. '
      elif sawItComin:
         message += ', and just as suspected, find themselves ambushed by a ' + monster_for_tile(game[IDX_map][tileIdx]) + '! '
      else:
         message += ', and while trying to rest are ambushed by a ' + monster_for_tile(game[IDX_map][tileIdx]) + '!'
      #  For now, auto-attack is always engaged when entering a tile with a monster on it
      if isMonster:
         message += '\n'
         message += do_ambush(sawItComin, game)
   return message

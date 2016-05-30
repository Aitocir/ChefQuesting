
import random

from combat import *
from constants import *
from generators import *
from game_utility import *

def game_verb_attack_results(player, game, connections):
   tile = game[IDX_map][game[IDX_location]]
   isMonster = tile & MASK_monster != 0
   message = do_attack_to_death(player[IDX_name], player[IDX_class], game)
   return message

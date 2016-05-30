
import random

from constants import *
from game_utility import *

def game_verb_search_results(pName, game, connections):
   # no args needed
   message = pName
   isMonster = game[IDX_map][game[IDX_location]] & MASK_monster != 0
   if isMonster:
      message += ' tries searching for ingredients, but is quickly deterred by the ' + monster_for_tile(game[IDX_map][game[IDX_location]]) + '.'
   else:
      advance_time(game)
      firstSearch = game[IDX_map][game[IDX_location]] & MASK_searched == 0
      luck = 0.5 if firstSearch else 0.1
      #  print 'set luck to: ',luck
      game[IDX_map][game[IDX_location]] = game[IDX_map][game[IDX_location]] | MASK_searched
      possTypes = set()
      if game[IDX_map][game[IDX_location]] & MASK_tree != 0:
         possTypes.add('leaves')
         possTypes.add('bark')
      if game[IDX_map][game[IDX_location]] & MASK_bush != 0:
         possTypes.add('root')
         possTypes.add('berries')
         possTypes.add('leaves')
      if game[IDX_map][game[IDX_location]] & MASK_flower != 0:
         possTypes.add('petal')
         possTypes.add('root')
         possTypes.add('leaves')
      todolist = game[IDX_todolist]
      possFinds = []
      for name, count in todolist.iteritems():
         for type in possTypes:
            if type in name:
               possFinds.append(name)
               #  print 'appended: ',name
      if len(possFinds) > 0 and luck > random.random():
         find = random.choice(possFinds)
         message += ' makes a royal mess of the area looking for ingredients until ' + time_of_day(game[IDX_time])
         message += ', and finds one ' + find + '! Booyah!'
         game[IDX_todolist][find] -= 1
         if game[IDX_todolist][find] <= 0:
            game[IDX_todolist].pop(find)
      else:
         message += ' drives everyone to dig and pull up everything in sight, but to no avail. It is now '
         message += time_of_day(game[IDX_time]) + ' and still no closer to being done.'
   return message

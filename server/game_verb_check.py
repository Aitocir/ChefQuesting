
from constants import *
from game_utility import *

def game_verb_check_results(game):
   needs = game[IDX_todolist]
   if len(needs) == 0:
      message = ' checks the ingredient list, and points out we have everything we need. Well done, team!\n\n'
      message += 'Congratulations on finishing a Chef Quest! You finished at ' + time_of_day(game[IDX_time])
      message += '. Play again and see if you can do it faster!\n\nYou are now back in the Lobby. '
      message += '[create] and new game, or [join] an existing one (leave the name blank to see what is available)'
      return message
   message = ' checks the ingredient list, and figures we still need to find:'
   for name, amnt in needs.iteritems():
      message += '\n' + str(amnt) + ' x ' + name
   return message

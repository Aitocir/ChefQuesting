#!/usr/bin/python           # This is server.py file

import socket
from thread import *
import time
import Queue
import random

# import other files from this package
from constants import *
from game_verb_attack import *
from game_verb_check import *
from game_verb_go import *
from game_verb_look import *
from game_verb_search import *
from game_utility import *
from generators import *
from network_twoway import *


def global_handler(game, connections, player, message):
   #  handler for 'rename' 'say' commands, which are valid and have consistent behavior in all contexts
   qPlayer = connections[player][IDX_qOut]
   words = message.split()
   if len(words) == 0:
      return True
   if words[0] == 'rename':
      oldName = connections[player][IDX_name]
      if len(words) > 1:
         rawName = words[1]
         cleanName = []
         for c in rawName:
            if ord(c) > 32 and ord(c) < 127:
               cleanName += c
         finalName = ''.join(cleanName)
         if len(finalName) > 0:
            #  good to go, change the name
            message = oldName + ' decided ' + finalName + ' sounds classier, and would like you to use it from here on out.'
            connections[player][IDX_name] = finalName
            send_message_to_game(game, message, connections, TYPE_info)
         else:
            #  send error, player tried to change name to something illegal
            errmsg = 'You tried to change your name to something beyond ASCII, as if Y2K was over and memory was cheap, or something. What a fool.'
            qPlayer.put(TYPE_info + errmsg)
      else:
         #  send error, player tried to change name but couldn't think of a good one and gave up
         errmsg = 'You tried to change your name, but failed to think of something cooler than ' + oldName + ' and gave up.'
         qPlayer.put(TYPE_info + errmsg)
   elif words[0] == 'say':
      restMsg = message[3:]
      finalMsg = connections[player][IDX_name] + ': \"' + restMsg.strip() + '\"'
      send_message_to_game(game, finalMsg, connections, TYPE_chat)
   else:
      return False
   return True

def lobby_handler(gameStates, connections, player, message):
   if global_handler(gameStates['Lobby'], connections, player, message):
      return
   words = message.split()
   qPlayer = connections[player][IDX_qOut]
   if len(words) == 0:
      return
   if words[0] == 'create':
      if len(words) < 3 or words[1] != 'as':
         msg = 'Invalid [create] usage. Should be "create as knight" or one of the other class types (augur, bandit, farmer).'
         qPlayer.put(TYPE_info + msg)
      #  create a game, put player in it
      elif words[2] in set(['knight', 'augur', 'bandit', 'farmer']):
         charInfo = tuple(CLASSES[words[2]])
         connections[player][IDX_class] = charInfo
         newName = generate_game_name(gameStates)
         newPlayers = set()
         newPlayers.add(player)
         gameStates[newName] = [newPlayers, generate_game_map(), MAP_start, 0, generate_game_ingredient_list(), 0, False]
         connections[player][IDX_gameId] = newName
         gameStates['Lobby'][IDX_players].remove(player)
         msg = 'Welcome to game ' + newName + '! Chat with your gamemates with [say] or start with a good [look] around.'
         qPlayer.put(TYPE_info + msg)
      else:
         err = '"' + words[2] + '" is not a valid class name.'
         qPlayer.put(TYPE_info + err)
   elif words[0] == 'join':
      if len(words) >= 4 and words[2] == 'as':
         #  search games for valid game name match
         joinedGame = False
         if words[3] in set(['knight', 'augur', 'bandit', 'farmer']):
            for name, data in gameStates.iteritems():
               if words[1] != 'Lobby':  #  no funny business, edge casers...
                  if words[1] == name:
                     #  join this game
                     #  1) set player game from Lobby to gameID
                     characterInfo = tuple(CLASSES[words[3]])
                     connections[player][IDX_class] = characterInfo
                     connections[player][IDX_gameId] = name
                     gameStates['Lobby'][IDX_players].remove(player)
                     send_message_to_game(gameStates['Lobby'], connections[player][IDX_name] + ' has left the lobby and joined game ' + name, connections, TYPE_info)
                     send_message_to_game(gameStates[name], connections[player][IDX_name] + ' has joined the game!', connections, TYPE_info)
                     gameStates[name][IDX_players].add(player)
                     #  2) suggest user start with look around since we're not giving a game-specific message here
                     msg = 'Welcome to game ' + name + '! Chat with your gamemates with [say] or start with a good [look] around.'
                     qPlayer.put(TYPE_info + msg)
                     joinedGame = True
            if not joinedGame:
               errmsg = 'You try to find a game named ' + words[1] + ' but fail. Perhaps you could have tea with your imaginary friends instead?'
               qPlayer.put(TYPE_info + errmsg)
      else:
         #  send message to player they need to provide a game name to join
         errmsg = '*** Command [join] needs a valid game name and class choice. A good example would be "join <game-name> as knight". '
         list = list_current_games(gameStates, connections)
         if len(list) == 0:
            errmsg += 'However, there are no games to join right now. You should [create] your own!'
         else:
            errmsg += 'The following games are available to join:\n' + list
         qPlayer.put(TYPE_info + errmsg)
   else:
      #  send message to user saying command words[0] not recognized
      errmsg = 'Command [' + words[0] + '] not recognized.'
      qPlayer.put(TYPE_info + errmsg)

def game_handler(game, lobby, connections, player, message):
   if global_handler(game, connections, player, message):
      return
   words = message.split()
   qPlayer = connections[player][IDX_qOut]
   if len(words) == 0:
      return
   elif words[0] == 'look':
      #  TODO: handle look verb, can have (north, south, west, east, around)
      if len(words) > 1:
         message = connections[player][IDX_class][IDX_NME] + ' ' + connections[player][IDX_name]
         message += game_verb_look_message(game[IDX_map], words[1], game[IDX_location], connections[player][IDX_class])
         send_message_to_game(game, message, connections, TYPE_narrative)
      else:
         #  TODO: throw error about missing direction
         errmsg = connections[player][IDX_name] + ' tries looking, but without in any particular direction, and ends up looking cross-eyed.'
         send_message_to_game(game, errmsg, connections, TYPE_narrative)
   elif words[0] == 'go':
      #  TODO: handle go verb, can have (north south east west as options, but must have one)
      if len(words) > 1:
         #  TODO: check words[1] for valid word
         result = game_verb_go_results(connections[player][IDX_name], game, words[1], connections)
         send_message_to_game(game, result, connections, TYPE_narrative)
      else:
         #  TODO: throw error about missing go object
         errmsg = connections[player][IDX_name] + ' tries to lead the team, but ends up going nowhere and looking kinda stupid.'
         send_message_to_game(game, errmsg, connections, TYPE_narrative)
   elif words[0] == 'attack':
      #  Engage with monster on this tile
      result = game_verb_attack_results(connections[player], game, connections)
      send_message_to_game(game, result, connections, TYPE_bad)
   elif words[0] == 'leave':
      #  Return player to game lobby
      connections[player][IDX_gameId] = 'Lobby'
      game[IDX_players].remove(player)
      lobby[IDX_players].add(player)
      msgGame = connections[player][IDX_name] + ' has left the game and returned to the Lobby.'
      send_message_to_game(game, msgGame, connections, TYPE_info)
      msgPlayer = 'You leave the game, and return to the Lobby. [create] your own game, or [join] to see what other games are running.'
      qPlayer.put(TYPE_info + msgPlayer)
   elif words[0] == 'check':
      #  report status of to-do list (later, may require argument so multiple things can be checked)
      result = connections[player][IDX_name] + game_verb_check_results(game)
      send_message_to_game(game, result, connections, TYPE_narrative)
      if 'ongratulations' in result:
         # game finished (yeah, this is ghetto, TODO to fix this later)
         for p in game[IDX_players]:
            connections[p][IDX_gameId] = 'Lobby'
            lobby[IDX_players].add(p)
         game[IDX_players] = set()
   elif words[0] == 'search':
      #  try to acquire an ingredient from this tile, fails if there's a monster
      result = game_verb_search_results(connections[player][IDX_name], game, connections)
      send_message_to_game(game, result, connections, TYPE_narrative)
   else:
      #  send message to user saying command words[0] not recognized
      errmsg = 'Command [' + words[0] + '] not recognized.'
      qPlayer.put(TYPE_info + errmsg)

def game_thread(qNewcomers):
   gameState = {}       #  'gameID' : (tuple of game info, including set of players in it, stateless metadata)
   connections = {}     #  'addr' : (name, gameID, qIn, qOut)
   lobbyPlayers = set()
   gameState['Lobby'] = [lobbyPlayers]
   while 1:
      time.sleep(0.02)
      while not qNewcomers.empty():
         noob = qNewcomers.get()
         connections[noob[0]] = [generate_player_name(), 'Lobby', noob[1], noob[2], ()]
         gameState['Lobby'][IDX_players].add(noob[0])
         welcome0 = 'Welcome to Aitocirs Chef Questing server! [create] a new game '
         welcomeMid = ''
         welcome1 = list_current_games(gameState, connections)
         if len(welcome1) == 0:
            welcomeMid = 'is really your only option as there are currently no other games to [join].'
         else:
            welcomeMid = 'or [join] any one of the following:\n\n'
         welcome = welcome0 + welcomeMid + welcome1
         noob[2].put(TYPE_info + welcome)
      removals = []
      for addr, data in connections.iteritems():
         if not data[IDX_qIn].empty():
            message = data[IDX_qIn].get()
            if len(message) == 0:
               gameState[data[IDX_gameId]][IDX_players].remove(addr)
               if len(gameState[data[IDX_gameId]][IDX_players]) == 0 and data[IDX_gameId] != 'Lobby':
                  #  destroy game, nobody is in it
                  gameState.pop(data[IDX_gameId])
               else:
                  send_message_to_game(gameState[data[IDX_gameId]], data[IDX_name] + ' has disconnected from the server.', connections, TYPE_info)
               removals.append(addr)
            elif data[IDX_gameId] == 'Lobby':
               lobby_handler(gameState, connections, addr, message)
            else:
               oldGame = data[IDX_gameId]  #  this might change after game_handler is done running
               game_handler(gameState[data[IDX_gameId]], gameState['Lobby'], connections, addr, message)
               if len(gameState[data[IDX_gameId]][IDX_players]) == 0 and data[IDX_gameId] != 'Lobby':
                  gameState.pop(data[IDX_gameId])
               if len(gameState[oldGame][IDX_players]) == 0 and oldGame != 'Lobby':
                  gameState.pop(oldGame)
               if gameState[data[IDX_gameId]][IDX_alert]:
                  gameState[data[IDX_gameId]][IDX_alert] = False
                  send_message_to_game(gameState[data[IDX_gameId]], describe_hunger(gameState[data[IDX_gameId]][IDX_hunger]), connections, TYPE_bad)
      for r in removals:
         connections.pop(r)
         print 'Lost connection with: ',r

s = socket.socket()         # Create a socket object
host = ''
port = 27243                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

connQueue = Queue.Queue()
start_new_thread(game_thread,(connQueue,))

while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from: ', addr
   qIn = Queue.Queue()
   qOut = Queue.Queue()
   start_new_thread(socket_inbound,(c,qIn,))
   start_new_thread(socket_outbound,(c,qOut,))
   addrStr = ''
   for e in addr:
      addrStr += str(e)
      addrStr += '::'
   connQueue.put((addrStr,qIn,qOut,))

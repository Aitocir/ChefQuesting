
import random

from constants import *
from game_utility import *

def describe_tile(map, tileIdx, playerClass):
   tile = map[tileIdx]
   hasTree = tile & MASK_tree != 0
   hasBush = tile & MASK_bush != 0
   hasFlower = tile & MASK_flower != 0
   hasMonster = tile & MASK_monster != 0
   beenSearched = tile & MASK_searched != 0
   beenVisited = tile & MASK_visited != 0
   beenSpied = tile & MASK_spied != 0
   opinion = tile & MASK_opinion
   features = []
   featureStr = ''
   if hasTree:
      features.append('some trees')
   if hasBush:
      features.append('some bushes')
   if hasFlower:
      features.append('some flowers')
   if len(features) == 0:
      featureStr = 'very little other than grass. '
   else:
      for i in range(len(features)):
         featureStr += features[i]
         if i != len(features) - 1:
            featureStr += ' and '
         else:
            featureStr += '. '
   conditionStr = 'It looks as if no human has ever been there. '
   if beenSearched:
      conditionStr = 'Your previous search efforts there make the view less appealing. '
   elif beenVisited:
      conditionStr = 'Your footprints are barely visible, but definitely there. '
   warningStr = ''
   if hasMonster:
      if beenVisited:
         #  you've been here before so there's no mystery, haven't killed it
         warningStr = 'The ' + monster_for_tile(tile) + ' is still there waiting for you.'
      elif beenSpied:
         #  Already tried guessing, echo earlier prediction found in opinion bool
         if opinion:
            warningStr = 'Although the view is beautful, earlier observations warrant caution.'
      else:
         #  make prediction based on chance
         isAware = random.random() < playerClass[IDX_NSF]
         if isAware:
            map[tileIdx] = map[tileIdx] | MASK_opinion
            warningStr = 'Strange sounds ruin the pristine view with a sense of danger.'
         else:
            map[tileIdx] = map[tileIdx] & ~MASK_opinion
   else:
      if beenVisited:
         pass
      elif beenSpied and opinion:
         warningStr = 'Although the view is beautful, earlier observations warrant caution.'
      else:
         isRight = random.random() < playerClass[IDX_SFE]
         if not isRight:
            map[tileIdx] = map[tileIdx] | MASK_opinion
            warningStr += 'Strange sounds ruin the pristine view with a sense of danger.'
         else:
            map[tileIdx] = map[tileIdx] & ~MASK_opinion
   map[tileIdx] = map[tileIdx] | MASK_spied
   return featureStr + conditionStr + warningStr

def game_verb_look_message(map, direction, currentIdx, playerClass):
   tileIdx = -1
   if direction == 'north':
      tileIdx = currentIdx - 16 if currentIdx - 16 > -1 else -2
   if direction == 'south':
      tileIdx = currentIdx + 16 if currentIdx + 16 < 256 else -2
   if direction == 'west':
      tileIdx = currentIdx - 1 if currentIdx % 16 != 0 else -2
   if direction == 'east':
      tileIdx = currentIdx + 1 if currentIdx % 16 != 15 else -2
   if direction == 'here':
      tileIdx = currentIdx
   message = ''
   if tileIdx == -2:
      message = ' gazes ' + direction + ', but sees nothing but a rocky drop-off and dark fog.'
   elif tileIdx == -1:
      message = ' tries to look ' + direction + ' before realizing foolishly ' + direction + ' might not be a direction after all.'
   else:
      message = ' looks ' + direction + ' and sees ' + describe_tile(map, tileIdx, playerClass)
   return message

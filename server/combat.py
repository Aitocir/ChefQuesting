
import random

from constants import *
from game_utility import *

def do_ambush(sawItComing, game):
    tile = game[IDX_map][game[IDX_location]]
    advance_time(game)
    game[IDX_hunger] += 1 if sawItComing else 2  #  combat accumulates extra hunger, moreso if ambushed
    message = 'The party fights into ' + time_of_day(game[IDX_time])
    message += ' to repel the initial attack' if sawItComing else ' with all their might to recover from the surprise attack'
    message += ', and can now decide whether to run away or '
    message += 'finish it off.' if sawItComing else 'fight back.'
    return message

def do_attack_to_death(pName, pClass, game):
    #  figure out how much time has to go by for this battle
    monsterHP = 8  #  TODO: monsters of different strengths
    tile = game[IDX_map][game[IDX_location]]
    game[IDX_map][game[IDX_location]] = tile & ~MASK_monster
    isMonster = tile & MASK_monster != 0
    message = ''
    if isMonster:
        #  TODO: combat
        baseAttack = pClass[IDX_DMG]
        multiplier = pClass[IDX_CRT]
        rounds = 0
        while monsterHP > 0:
            rounds += 1
            roll = d20()
            damage = int(float(baseAttack) * (multiplier ** float(roll)))
            monsterHP -= damage
            advance_time(game)
            game[IDX_hunger] += 1  #  combat costs extra hunger
            message += pName + ' strikes at the ' + monster_for_tile(tile) + ', '
            message += 'dealing ' + str(damage) + ' damage. '
            if monsterHP > 0:
                message += 'The ' + monster_for_tile(tile) + ' stands its ground, as the battle goes into the '
                message += time_of_day(game[IDX_time]) + ', driving up the party\'s hunger.'
            else:
                message += 'The ' + monster_for_tile(tile) + ' sways, then falls to the ground, '
                if rounds == 1:
                    message += 'soundly defeated in record time. '
                elif rounds == 2:
                    message += 'beaten in an awful half-day of battle. '
                else:
                    message += 'finally put down after what seemed like an eternity of battle. '
            message += '\n'
        message += 'With the battle over, the quest continues in the ' + time_of_day(game[IDX_time]) + '.'
    else:
        message += pName
        message += ' brandishes their weapon at random surrounding plant life before realizing there is no monster here.'
    return message

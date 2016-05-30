
import random

#  intra-package
from constants import *


def generate_game_tile():
   valTree = MASK_tree if random.random() < 0.3 else 0
   valBush = MASK_bush if random.random() < 0.3 else 0
   valFlower = MASK_flower if random.random() < 0.3 else 0
   valMonster = MASK_monster if random.random() < 0.5 else 0
   #  other bits are generically 0, caller might modify for starting tile exceptions
   tile = valTree + valBush + valFlower + valMonster
   return tile

def generate_game_map():
   tiles = []
   for i in range(256):
      t = generate_game_tile()
      if i == MAP_start:
         t = t | MASK_visited
         t = t & ~MASK_monster
         t = t | MASK_spied
      tiles.append(t)
   return tiles

def generate_game_ingredient_list():
   types = ['leaves', 'root', 'berries', 'bark', 'petals']
   names = ['Abak', 'Blappe', 'Copoa', 'Urmoi', 'Reeq', 'Soll', 'Vunit']
   ingredients = []
   for i in range(5):
      ingredients.append(random.choice(names) + ' ' + random.choice(types))
   ingList = {}
   for i in range(5):
      ingList[ingredients[i]] = 0
   for i in range(5):
      ingList[ingredients[i]] += 1
   return ingList

def generate_game_name(existingGameStates):
   adj0 = ['Tiny', 'Small', 'Huge', 'Massive', 'Scary', 'Funny', 'Weird', 'Boring', 'Crazy', 'Cold', 'Hot', 'Loud', 'Silent']
   adj1 = ['Red', 'Scarlet', 'Orange', 'Yellow', 'Green', 'Blue', 'Cyan', 'Teal', 'Purple', 'White', 'Black', 'Brown', 'Pink', 'Gray', 'Tan', 'Amber', 'Gold', 'Silver', 'Chrome']
   noun = ['Coin', 'Stamp', 'Card', 'Lamp', 'Wave', 'Phone', 'Bench', 'Rock', 'Stone', 'Boat', 'Bird', 'Plant', 'Pot', 'Fish', 'Dog', 'Cat', 'Shoe']
   name = ''
   unique = False
   existingNames = set(existingGameStates.keys())
   while not unique:
      name = random.choice(adj0)
      name += random.choice(adj1)
      name += random.choice(noun)
      unique = name not in existingNames
   return name

def generate_player_name():
    titles = ['Captain', 'Liuetenant', 'Chief', 'Commander', 'Colonel', 'Sergeant', 'Master', 'Darth', 'President', 'Doctor', 'Director', 'Officer', 'General'];
    names = ['Platypus', 'Orangutan', 'Seahorse', 'Aardvark', 'Flamingo','Penguin','Armadillo','Raccoon','Llama','Giraffe','Unicorn','Dragon','Butterfly'];
    name = ''
    name += random.choice(titles)
    name += random.choice(names)
    return name

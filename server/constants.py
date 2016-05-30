#  game metadata
IDX_players = 0         # index for set of participating playerIDs
IDX_map = 1             # (GAME ONLY) index for map, list of integers
IDX_location = 2        # (GAME ONLY) index for players' location on map (0-255 as list index of map)
IDX_time = 3            # (GAME ONLY) index for players' day and time (0+ int, mod 8 shows time, div by 8 plus 1 shows day)
IDX_todolist = 4        # (GAME ONLY) index for players' ingredient list, dict of string:int (item-name:item-count-remaining-to-find)
IDX_hunger = 5          # (GAME ONLY) index for players' hunger (death if >= x)
IDX_alert = 6           # (GAME ONLY) an alert is pending for the game (hunger only for now)

#  player metadata
IDX_name = 0            # index for player's screen name (not unique)
IDX_gameId = 1          # index of gameID player is currently in
IDX_qIn = 2             # index for player's inbound message queue
IDX_qOut = 3            # index for player's outbound message queue
IDX_class = 4           # index for player's class information

#  class definitions
CLASSES = {
'knight':[14, 1.02, 0.01, 0.5, 1.04, 0.75, 0.75, 3, 0.8, 'Knight'],
'augur' :[ 4, 1.04, 0.15, 0.6, 1.04, 0.90, 1.00, 2, 0.8, 'Augur'],
'bandit':[ 6, 1.07, 0.85, 0.6, 1.04, 0.75, 0.75, 2, 0.8, 'Bandit'],
'farmer':[ 4, 1.04, 0.15, 0.9, 1.09, 0.75, 0.75, 2, 1.0, 'Farmer']}

#  Class information
IDX_DMG = 0           # index for base attack (int)
IDX_CRT = 1           # index for critical multiplier (raised by d20 roll)
IDX_SNK = 2           # index for sneak chances (%)
IDX_ING = 3           # index for chances of finding ingredients (%)
IDX_FOD = 4           # index for food finding multiplier
IDX_SFE = 5           # index for chances of correctly interpreting a safe tile
IDX_NSF = 6           # index for chances of correctly interpreting an unsafe tile
IDX_APT = 7           # index for how much food fills you up
IDX_COK = 8           # chances of cooking food successfully on the first try
IDX_NME = 9           # proper name of class

#  bitmasks for map information
MASK_tree = 1         # bitmask value for (no|some) trees, immutable
MASK_bush = 2         # bitmask value for (no|some) bushes, immutable
MASK_flower = 4       # bitmask value for (no|some) flowers, immutable
MASK_monster = 8      # bitmask value for (0|1) monsters, cleared when killed
MASK_searched = 16    # bitmask value for (hasn't|has) searched here yet, always starts 0
MASK_visited = 32     # bitmask value for (hasn't|has) been here before, always starts 0 except start tile
MASK_spied = 64       # bitmask value for (hasn't|has) looked here before, when 1 monster predicts locked
MASK_opinion = 128    # bitmask value for thinking there (isn't|is) monster here; set on first spy, used after

MAP_start = 120       # map index players start off at

#  message type codes
TYPE_info = chr(0)
TYPE_good = chr(1)
TYPE_bad = chr(2)
TYPE_narrative = chr(3)
TYPE_chat = chr(4)

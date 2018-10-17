#!/usr/bin/env python3
# Python 3.6

import hlt
from hlt import constants
from hlt.positionals import Direction
import random
import logging # Logging allows you to save messages for yourself. This is required because the regular STDOUT
import numpy as np

""" <<<Game Begin>>> """

game = hlt.Game()
game.ready("Bot v1")
me = game.me
"""
    Strategy :
     > Collect Halite : 0
     > Attack : 1
     > Produce Ships: 2
     > Create Dropoff Points : 3
"""
logging.info("Successfully created bot! My Player ID is {}.".format(game.my_id))
ship_status = {}

def CommandQueue():
     # You extract player metadata and the updated map metadata here for convenience.
    me = game.me
    game_map = game.game_map
    command_queue = []
    directions = [Direction.North, Direction.South,Direction.East, Direction.West]
    for ship in me.get_ships():
        logging.info("Ship {} has {} halite.".format(ship.id, ship.halite_amount))

        if ship.id not in ship_status:
            ship_status[ship.id] = "exploring"

        if ship_status[ship.id] == "returning":
            if ship.position == me.shipyard.position:
                ship_status[ship.id] = "exploring"
            else:
                move = game_map.naive_navigate(ship, me.shipyard.position)
                command_queue.append(ship.move(move))
                continue
        elif ship.halite_amount >= constants.MAX_HALITE / 4:
            ship_status[ship.id] = "returning"


        if game_map[ship.position].halite_amount < constants.MAX_HALITE / 10 or ship.is_full:
            pick = random.choice(directions) if directions else Direction.North
            directions = directions.remove(pick) if directions else [Direction.North, Direction.South,Direction.East, Direction.West]
            command = game_map.naive_navigate(ship, ship.position.directional_offset(pick))
            command_queue += [ship.move(command)]
        else:
            command_queue.append(ship.stay_still())
    if game.turn_number <= 200 and me.halite_amount >= constants.SHIP_COST and not game_map[me.shipyard].is_occupied:
        command_queue.append(me.shipyard.spawn())
    
    return command_queue
""" <<<Game Loop>>> """
while True:
    game.update_frame()
    command_queue = CommandQueue()
    game.end_turn(command_queue)

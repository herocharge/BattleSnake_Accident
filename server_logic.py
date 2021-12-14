#go to server_logic_v2
from typing import List, Dict

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""
orientation = ""
i = 0 


def path_to_food(my_head, food, possible_moves):
  global i
  if my_head["x"] > food[i]["x"]:
      move = "left"
  elif my_head["x"] < food[i]["x"]:
      move = "right"
  elif my_head["y"] > food[i]["y"]:
      move = "down"
  elif my_head["y"] < food[i]["y"]:
      move = "up"
  if move in possible_moves:
    i=0
    print('1')
    return move
  elif len(food)-1>i:
    i+=1
    print("2")
    #print(i)
    return path_to_food(my_head, food, possible_moves)
  else:
    i=0
    print("3")
    return possible_moves[0]


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
  
    """
    my_head: Dictionary of x/y coordinates of the Battlesnake head.
            e.g. {"x": 0, "y": 0}
    my_body: List of dictionaries of x/y coordinates for every segment of a Battlesnake.
            e.g. [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    possible_moves: List of strings. Moves to pick from.
            e.g. ["up", "down", "left", "right"]

    return: The list of remaining possible_moves, with the 'neck' direction removed
    """


    
    if {"x": my_head["x"], "y": my_head["y"]+1} in my_body or my_head["y"] == 10:
      possible_moves.remove("up")
  
    if {"x": my_head["x"], "y": my_head["y"]-1} in my_body or my_head["y"] == 0:
      possible_moves.remove("down")
  
    if {"x": my_head["x"]+1, "y": my_head["y"]} in my_body or my_head["x"] == 10:
      possible_moves.remove("right")
  
    if {"x": my_head["x"]-1, "y": my_head["y"]} in my_body or my_head["x"] == 0:
      possible_moves.remove("left")

    #print(possible_moves)
    return possible_moves


def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board
    for each move of the game.

    """
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]
     # A list of x/y coordinate dictionaries like [ {"x": 0, "y": 0}, {"x": 1, "y": 0}, {"x": 2, "y": 0} ]
    food = data["board"]["food"]
    # TODO: uncomment the lines below so you can see what this data looks like in your output!
    # print(f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~")
    # print(f"All board data this turn: {data}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")

    possible_moves = ["up", "down", "left", "right"]
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves)
    # possible_moves = avoid_my_neck()
    move = path_to_food(my_head, food, possible_moves)
    #print(data["board"]["width"])
    return move
    
    


    

    # Don't allow your Battlesnake to move back in on it's own neck
    # possible_moves = avoid_my_neck(my_head, my_body, possible_moves)

    # TODO: Using information from 'data', find the edges of the board and don't let your Battlesnake move beyond them
    # board_height = ?
    # board_width = ?

    # TODO Using information from 'data', don't let your Battlesnake pick a move that would hit its own body

    # TODO: Using information from 'data', don't let your Battlesnake pick a move that would collide with another Battlesnake

    # TODO: Using information from 'data', make your Battlesnake move towards a piece of food on the board
    # move = possible_moves[possible_moves.index(orientation) + 1]
    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    # board_width = data["board"]["width"]
    
    # TODO: Explore new strategies for picking a move that are better than random

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move

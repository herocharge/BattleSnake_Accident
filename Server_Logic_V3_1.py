''' ----- deprioritise moving near the head of other snake instead of completely ruling out '''

from typing import List, Dict


orientation = ""
i = 0 
k = 0
last_choice_moves = ["up", "down", "left", "right"]

def Distance_between(t1,t2): # it takes two tuples storing the coordinates
  Dist = ((t1["x"] - t2["x"])**2 + (t1["y"] - t2["y"])**2)**0.5
  return Dist



def path_to_food(my_head, food, possible_moves):
  global last_choice_moves
  print()
  global i,k

  Dist_to_food = []
  for j in range(len(food)):
    Dist = Distance_between(my_head,food[j])
    Dist_to_food.append((Dist,j))

  Dist_to_food.sort()
  
  
  move = "right"
  if len(Dist_to_food)>k:
    if my_head["x"] > food[Dist_to_food[k][1]]["x"]:
        move = "left"
    elif my_head["x"] < food[Dist_to_food[k][1]]["x"]:
        move = "right"
    elif my_head["y"] > food[Dist_to_food[k][1]]["y"]:
        move = "down"
    elif my_head["y"] < food[Dist_to_food[k][1]]["y"]:
        move = "up"
  # print(len(food))
  if move in possible_moves:
    k=0
    print('1')
    return move
  elif len(food)-1>k:
    k+=1
    print("2")
    #print(i)
    return path_to_food(my_head, food, possible_moves)
  else:
    k=0
    print("3")
    return last_choice_moves[0]


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str], board_height, board_width, snakes, my_id) -> List[str]:
  
    global near_enemy_head, last_choice_moves
     
    near_enemy_head = []
    for snake in snakes:
      if snake["id"] != my_id:
        my_body += snake["body"]

        near_enemy_head += [{'x' : snake["body"][0]["x"]+1, 'y' : snake["body"][0]["y"]},
                  {'x' : snake["body"][0]["x"], 'y' : snake["body"][0]["y"]+1},
                  {"x" : snake["body"][0]["x"], "y" : snake["body"][0]["y"]-1},
                  {"x" : snake["body"][0]["x"]-1, "y" : snake["body"][0]["y"]}]


    near_enemy_head.append(my_body[len(my_body)-1])

    
    if {"x": my_head["x"], "y": my_head["y"]+1} in my_body or my_head["y"] == (board_height-1):
      possible_moves.remove("up")
      last_choice_moves.remove("up")
    elif {"x": my_head["x"], "y": my_head["y"]+1} in near_enemy_head:
      possible_moves.remove("up")
      last_choice_moves.remove("up")
      last_choice_moves.append("up")

  
    if {"x": my_head["x"], "y": my_head["y"]-1} in my_body or my_head["y"] == 0:
      possible_moves.remove("down")
      last_choice_moves.remove("down")
    elif {"x": my_head["x"], "y": my_head["y"]-1} in near_enemy_head:
      possible_moves.remove("down")
      last_choice_moves.remove("down")
      last_choice_moves.append("down")

  
    if {"x": my_head["x"]+1, "y": my_head["y"]} in my_body or my_head["x"] == (board_width-1):
      possible_moves.remove("right")
      last_choice_moves.remove("right")
    elif {"x": my_head["x"]+1, "y": my_head["y"]} in near_enemy_head:
      possible_moves.remove("right")
      last_choice_moves.remove("right")
      last_choice_moves.append("right")

  
    if {"x": my_head["x"]-1, "y": my_head["y"]} in my_body or my_head["x"] == 0:
      possible_moves.remove("left")
      last_choice_moves.remove("left")
    elif {"x": my_head["x"]-1, "y": my_head["y"]} in near_enemy_head:
      possible_moves.remove("left")
      last_choice_moves.remove("left")
      last_choice_moves.append("left")


    print(possible_moves)
    #print(my_body)
    #print(last_choice_moves)
    return possible_moves


def choose_move(data: dict) -> str:
    
    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]


    food = data["board"]["food"]

    my_id = data["you"]["id"]


    snakes = data["board"]["snakes"]
    possible_moves = ["up", "down", "left", "right"]

    global last_choice_moves

    last_choice_moves = ["up", "down", "left", "right"]
    possible_moves = avoid_my_neck(my_head, my_body, possible_moves, data["board"]["height"], data["board"]["width"], snakes, my_id)
    # possible_moves = avoid_my_neck()
    move = path_to_food(my_head, food, possible_moves)
    return move
    
    

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move

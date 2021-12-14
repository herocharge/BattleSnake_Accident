''' ------------------- TO BE SCRAPPED ----------------

---------1) attempt to resolve the self looping issue by quadrant method
---------2) deprioritise moving near the head of other snake instead of completely ruling out '''


from typing import List, Dict


orientation = ""
i = 0 
k = 0
possible_moves = ["up", "down", "left", "right"]
last_choice_moves = ["up", "down", "left", "right"]


def most_frequent(Array):
    return max(set(Array), key = Array.count)

'''
def Find_Quadrant(body,board_height,board_width): # finds the quadrant of snake
  
  snake_quadrants = []
  for part in body:

    if part["x"] > board_width/2 and part["y"] > board_height/2:
      Quadrant = 1
      part

    elif part["x"] < board_width/2 and part["y"] > board_height/2:
      Quadrant = 2

    elif part["x"] < board_width/2 and part["y"] < board_height/2:
      Quadrant = 3

    else:
      Quadrant = 4

    return most_frequent(snake_quadrants)
'''  


def Distance_between(t1,t2): # it takes two tuples storing the coordinates
  Dist = ((t1["x"] - t2["x"])**2 + (t1["y"] - t2["y"])**2)**0.5
  return Dist



def path_to_food(my_head, food, possible_moves):
  print("test")
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
  elif len(food)-1>i:
    k+=1
    print("2")
    #print(i)
    return path_to_food(my_head, food, possible_moves)
  else:
    k=0
    print("3")  
    return last_choice_moves[0]


def avoid_my_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str], board_height, board_width, snakes, my_id) -> List[str]:
  
    global last_choice_moves
    
    near_enemy_head = []
    for snake in snakes:
      if snake["id"] != my_id:
        my_body+=snake["body"]
        near_enemy_head += [{'x' : snake["body"][0]["x"]+1, 'y' : snake["body"][0]["y"]},
                  {'x' : snake["body"][0]["x"], 'y' : snake["body"][0]["y"]+1},
                  {"x" : snake["body"][0]["x"], "y" : snake["body"][0]["y"]-1},
                  {"x" : snake["body"][0]["x"]-1, "y" : snake["body"][0]["y"]}]
        
    #print(my_body)
    # my_quadrant = Find_Quadrant(my_body,board_height,board_width)
    
    
    if {"x": my_head["x"], "y": my_head["y"]+1} in my_body or my_head["y"] == (board_height-1) :
      possible_moves.remove("up")
      last_choice_moves = list(possible_moves)
      
    elif {"x": my_head["x"], "y": my_head["y"]+1} in near_enemy_head:
      possible_moves.remove("up")
      last_choice_moves = list(possible_moves)
      last_choice_moves.append("up")
  
    if {"x": my_head["x"], "y": my_head["y"]-1} in my_body or my_head["y"] == 0:
      possible_moves.remove("down")
      last_choice_moves = list(possible_moves)

    elif {"x": my_head["x"], "y": my_head["y"]+1} in near_enemy_head:
      possible_moves.remove("down")
      last_choice_moves = list(possible_moves)
      last_choice_moves.append("down")
  
    if {"x": my_head["x"]+1, "y": my_head["y"]} in my_body or my_head["x"] == (board_width-1):
      possible_moves.remove("right")
      last_choice_moves = list(possible_moves)

    elif {"x": my_head["x"], "y": my_head["y"]+1} in near_enemy_head:
      possible_moves.remove("right")
      last_choice_moves = list(possible_moves)
      last_choice_moves.append("right")
  
    if {"x": my_head["x"]-1, "y": my_head["y"]} in my_body or my_head["x"] == 0:
      possible_moves.remove("left")
      last_choice_moves = list(possible_moves)

    elif {"x": my_head["x"], "y": my_head["y"]+1} in near_enemy_head:
      possible_moves.remove("left")
      last_choice_moves = list(possible_moves)
      last_choice_moves.append("left")


    

    print(possible_moves)
    return possible_moves, last_choice_moves


def choose_move(data: dict) -> str:

    my_head = data["you"]["head"]  # A dictionary of x/y coordinates like {"x": 0, "y": 0}
    my_body = data["you"]["body"]

    food = data["board"]["food"]

    my_id = data["you"]["id"]

    snakes = data["board"]["snakes"]
    possible_moves = ["up", "down", "left", "right"]
    last_choice_moves = ["up", "down", "left", "right"]

    possible_moves, last_choice_moves = avoid_my_neck(my_head, my_body, possible_moves, data["board"]    ["height"], data["board"]["width"], snakes, my_id)

    move = path_to_food(my_head, food, possible_moves)
    return move
    

    print(f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}")

    return move


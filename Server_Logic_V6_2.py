''' ---------------- run along ACTUAL perimeter if necessary'''
# up  = 0
# down = 1
# left = 2
# right = 3

from typing import List, Dict


points = [0, 0, 0, 0]
snakes = {}
my_body = []
HEIGHT = 0
WIDTH = 0
SHIFTLENGTH = 10
SHIFTHEALTH = 60 # TO BE CHANGED TO 60

DEATH = -100000
EATMYTAILFACTOR = 200
HEADWINFACTOR = -10  #CHANGED FROM 0 TO -10
HEADLOSEFACTOR = 10000
FOODFACTOR = 1
FREESPACEFACTOR = 30 #
PERIMETERFACTOR = 200



def head_check(pos, my_id):

  position = {"x" : pos["x"], "y" : pos["y"]}

  
  for snake in snakes:
    
    if snake["id"] != my_id:
      near_enemy_head = [{'x' : snake["body"][0]["x"]+1, 'y' : snake["body"][0]["y"]},
                      {'x' : snake["body"][0]["x"], 'y' : snake["body"][0]["y"]+1},
                      {"x" : snake["body"][0]["x"], "y" : snake["body"][0]["y"]-1},
                      {"x" : snake["body"][0]["x"]-1, "y" : snake["body"][0]["y"]}]

      if position in near_enemy_head:
        if len(my_body) > len(snake["body"]):
          points[pos["index"]] += HEADWINFACTOR
          break

        else:
          points[pos["index"]] -= HEADLOSEFACTOR
          break  
  


def Distance_between(t1,t2): # it takes two tuples storing the coordinates
  Dist = ((t1["x"] - t2["x"])**2 + (t1["y"] - t2["y"])**2)**0.5
  return Dist


def death_check(pos, my_id):
  # print(pos["index"])
  if(pos["x"] >= WIDTH or pos["x"] < 0 or pos["y"] < 0 or pos["y"] >= HEIGHT): # boundary check
    points[pos["index"]]+=DEATH
    return

  for s in snakes:
    # print(s)
    if my_id != s["id"]:
      if {"x": pos["x"] , "y":pos["y"]} in s["body"]:
        points[pos["index"]]+=DEATH
        # print(pos["index"])
        return
  if {"x": pos["x"], "y":pos["y"]} in my_body[0:len(my_body)-1]:
    points[pos["index"]] += DEATH
    return
  
  if {"x": pos["x"], "y":pos["y"]} in list(my_body[len(my_body)-1]) and HEALTH ==100:
    points[pos["index"]] += EATMYTAILFACTOR

def food_check(pos, food):
    position = {"x" : pos["x"], "y" : pos["y"]}
    dist =  Distance_between(position, food)
    points[pos["index"]]-=(dist)*FOODFACTOR


def free_space(pos,my_id):
  position = {"x" : pos["x"], "y" : pos["y"]}
  free_count = 4
  north = {"x" : position["x"], "y" : position["y"]+1}
  south = { "x" : position["x"], "y" : position["y"]-1} 
  west = {"x" : position["x"]-1, "y" : position["y"]}
  east = {"x" : position["x"]+1, "y" : position["y"]}

  for snake in snakes:
      if north in snake["body"]:
        free_count-=1
      if south in snake["body"]:
        free_count-=1
      if west in snake["body"]:
        free_count-=1
      if east in snake["body"]:
        free_count-=1

  if not pos["y"] in range(HEIGHT):
    free_count-=1
  if not pos["x"] in range(WIDTH):
    free_count-=1
  
  
  points[pos["index"]]+=free_count*FREESPACEFACTOR

def move_to_perimeter(pos):
  x = pos["x"]
  y = pos["y"]


  points[pos["index"]] += max(abs(x-1), abs(x-WIDTH+2), abs(y-HEIGHT+2), abs(y-1))*PERIMETERFACTOR

  if(x == 0 or x == WIDTH-1 or y == 0 or y == HEIGHT-1):
    points[pos["index"]] -= max(abs(x-1), abs(x-WIDTH+2), abs(y-HEIGHT+2), abs(y-1))*PERIMETERFACTOR
  
    points[pos["index"]] += max(abs(x-1), abs(x-WIDTH+2), abs(y-HEIGHT+2), abs(y-1))*PERIMETERFACTOR*(WIDTH-2)/(WIDTH)
  
''''
  if(x == 0 or x == WIDTH-1 or y == 0 or y == HEIGHT-1):
    points[pos["index"]] -= max(abs(x-1), abs(x-WIDTH+2), abs(y-HEIGHT+2), abs(y-1))*PERIMETERFACTOR

  elif(x == 2 or y == WIDTH-3 or y == 2 or y == HEIGHT-3):
    points[pos["index"]] -= max(abs(x-1), abs(x-WIDTH+2), abs(y-HEIGHT+2), abs(y-1))*3*PERIMETERFACTOR/2

'''

def choose_move(data: dict) -> str:
  global HEIGHT
  global WIDTH
  global points
  global my_body
  global snakes
  global SHIFTLENGTH, SHIFTHEALTH, HEALTH


  HEALTH = data["you"]["health"]
  HEIGHT = data["board"]["height"]
  WIDTH  = data["board"]["width"]
  SHIFTLENGTH = 3*HEIGHT/4

  moves = ["up", "down", "left", "right"];
  points = [0, 0, 0, 0]
  my_body = data["you"]["body"]
  my_head = data["you"]["body"][0]
  snakes = data["board"]["snakes"]
  # snakes += data["you"]["body"]
  index = {
          "up": {"index": 0 , "x" : my_head["x"], "y" : my_head["y"]+1}, 
          "down" : {"index": 1 , "x" : my_head["x"], "y" : my_head["y"]-1}, 
          "left" : {"index": 2 , "x" : my_head["x"]-1, "y" : my_head["y"]}, 
          "right" : {"index": 3 , "x" : my_head["x"]+1, "y" : my_head["y"]}
        }
  closest_food = {}
  is_there_food = 1
  if(len(data["board"]["food"]) > 0):
    closest_food = data["board"]["food"][0]
    for f in data["board"]["food"]:
      if(Distance_between(my_head, f) < Distance_between(my_head, closest_food)):
        closest_food = f
  else:
    is_there_food = 0

  for m in moves:
    death_check(index[m], data["you"]["id"])
    if(is_there_food):
      food_check(index[m], closest_food)
    
    head_check(index[m],data["you"]["id"])
    
    if len(my_body)>SHIFTLENGTH and data["you"]["health"]>SHIFTHEALTH:
      print('called')
      move_to_perimeter(index[m])
    else:
      free_space(index[m],data["you"]["id"])


  move = ""
  max = -1000000
  ind = 0
  print(points)
  for i in range(4):
    if(points[i]>max):
      max = points[i]
      ind = i
  
  move = moves[ind]

  return move

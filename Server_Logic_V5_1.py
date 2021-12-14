''' ----------------- TO BE SCRAPPED-------------
--------- attempt to avoid loops Turncounter method'''
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

DEATH = -100
FOODFACTOR = 3
FREESPACEFACTOR = 10
TURNFACTOR = -5
TURNFACTOR_X = 0
TURNFACTOR_Y = 0 

def Distance_between(t1,t2): # it takes two DICTIONARIES storing the coordinates
  Dist = ((t1["x"] - t2["x"])**2 + (t1["y"] - t2["y"])**2)**0.5
  return Dist

def death_check(pos):
  if(pos["x"] >= WIDTH or pos["x"] < 0 or pos["y"] < 0 or pos["y"] >= HEIGHT):
    points[pos["index"]]+=DEATH
    return
  for s in snakes:
    if {"x": pos["x"], "y":pos["y"]} in s["body"]:
      points[pos["index"]]+=DEATH
      return
  if {"x": pos["x"], "y":pos["y"]} in my_body:
      points[pos["index"]]+=DEATH
      return

def food_check(pos, food):
    position = {"x" : pos["x"], "y" : pos["y"]}
    dist =  Distance_between(position, food)
    points[pos["index"]]-=(dist)*FOODFACTOR

def free_space(pos):
  position = {"x" : pos["x"], "y" : pos["y"]}
  free_count = 4
  north = {"x" : position["x"], "y" : position["y"]+1}
  south = { "x" : position["x"], "y" : position["y"]-1} 
  west = {"x" : position["x"]-1, "y" : position["y"]}
  east = {"x" : position["x"]+1, "y" : position["y"]}

  for snake in snakes:
    if north in snake["body"] or north in my_body:
      free_count-=1
    if south in snake["body"] or south in my_body:
      free_count-=1
    if west in snake["body"] or west in my_body:
      free_count-=1
    if east in snake["body"] or east in my_body:
      free_count-=1
  if not pos["y"] in range(HEIGHT):
    free_count-=1
  if not pos["x"] in range(WIDTH):
    free_count-=1
  
  if north in my_body:
     free_count-=1
  if south in my_body:
     free_count-=1
  if west in my_body:
     free_count-=1
  if east in my_body:
     free_count-=1
  points[pos["index"]]+=free_count*FREESPACEFACTOR

'''
def avoid_loop(move):
  global TURNFACTOR_X, TURNFACTOR_Y
  if move == "right":
    TURNFACTOR_X += 1

  elif move == "left":
    TURNFACTOR_X -= 1
  
  elif move == "down":
    TURNFACTOR_Y -= 1

  else:
    TURNFACTOR_Y += 1

  if TURNFACTOR_X % 4 == 0:
    TURNFACTOR_X = 0

  if TURNFACTOR_Y % 4 == 0:
    TURNFACTOR_Y = 0

  if TURNFACTOR_X > 0:
    points[3] += TURNFACTOR*TURNFACTOR_X

  elif TURNFACTOR_X < 0:
     points[2] -= TURNFACTOR*TURNFACTOR_X

  if TURNFACTOR_Y > 0:
    points[0] += TURNFACTOR*TURNFACTOR_Y
  
  elif TURNFACTOR_Y < 0:
    points[1] -= TURNFACTOR*TURNFACTOR_Y
'''



def choose_move(data: dict) -> str:
  global HEIGHT
  global WIDTH
  global points
  global my_body
  HEIGHT = data["board"]["height"]
  WIDTH  = data["board"]["width"]

  moves = ["up", "down", "left", "right"];
  points = [0, 0, 0, 0]
  my_body = data["you"]["body"]
  my_head = data["you"]["body"][0]
  snakes = data["board"]["snakes"]
  snakes += data["you"]["body"]
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
      if(Distance_between(my_head, f) > Distance_between(my_head, closest_food)):
        closest_food = f
  else:
    is_there_food = 0

  for m in moves:
    death_check(index[m])
    if(is_there_food):
      food_check(index[m], data["board"]["food"][0])
    free_space(index[m])


  move = ""
  max = -1000000
  ind = 0
  for i in range(4):
    if(points[i]>max):
      max = points[i]
      ind = i
  
  move = moves[ind]

  return move

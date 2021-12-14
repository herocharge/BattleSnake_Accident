''' ---------------- MORE AREA'''
# up  = 0
# down = 1
# left = 2
# right = 3

from typing import List, Dict


points = [0, 0, 0, 0]
snakes = {}
my_body = []
HEIGHT = 10
WIDTH = 10#hey! 
SHIFTLENGTH = 10
SHIFTHEALTH = 60 # TO BE CHANGED TO 60

DEATH = -10000000
EATMYTAILFACTOR = 200
HEADWINFACTOR = 0  #CHANGED FROM 0 TO -10
HEADLOSEFACTOR = 10000
FOODFACTOR = 1
FREESPACEFACTOR = 0
PERIMETERFACTOR = 10 # CHANGED FROM 200
AREAFACTOR = 0


grid = []

areas = {}


def area_check(pos):
  temp = []
  for i in grid:
    temp += i
  if grid[pos["x"]][pos["y"]] != -1:
    points[pos["index"]]+=temp.count(grid[pos["x"]][pos["y"]])*AREAFACTOR
  

def rec(point, value):
  if(grid[point["x"]][point["y"]] != 0):
    return
  else:
    x = point["x"]
    y = point["y"]
    grid[x][y] = value
    rec({"x" : x+1, "y" : y  }, value)
    rec({"x" : x-1, "y" : y  }, value)
    rec({"x" : x,   "y" : y+1}, value)
    rec({"x" : x,   "y" : y-1}, value)

def grid_generation():
  for i in range(1, WIDTH+2):
    for j in range (1, HEIGHT+2):
      grid[i][j] = 0

    
  # print(grid)
  for s in snakes:
    for part in s["body"]:
      grid[part["x"]][part["y"]] = -1
      grid[part["x"]][part["y"]] = -1
  
  for i in range(HEIGHT+2):
    
    grid[0][i] = -1
    grid[WIDTH+1][i] = -1

  for i in range (WIDTH + 2):
    grid[i][0] = -1
    grid[i][HEIGHT+1] = -1
    
  counter = 1
  # grid[1][1] = counter
  
  for i in range(1, WIDTH+1):
    for j in range(1, HEIGHT+1):
     
      if grid[i][j] == 0:
        counter+=1
        rec({"x":i, "y":j}, counter)
        
  # for i in range(0, HEIGHT+2):
  #   for j in range (0, WIDTH+2):
  #     if grid[j][i] == -1:
  #       print('#', end = " ")
  #     else:
  #       print(grid[j][i], end = " ")
  #   print()

  
  

  # print(areas)
          
def head_check(pos, my_id):

  position = {"x" : pos["x"], "y" : pos["y"]}

  
  for snake in snakes:
    
    if snake["id"] != my_id:
      near_enemy_head = [{'x' : snake["body"][0]["x"]+1, 'y' : snake["body"][0]["y"]},
                      {'x' : snake["body"][0]["x"], 'y' : snake["body"][0]["y"]+1},
                      {"x" : snake["body"][0]["x"], "y" : snake["body"][0]["y"]-1},
                      {"x" : snake["body"][0]["x"]-1, "y" : snake["body"][0]["y"]}]

      if position in near_enemy_head:
        # if len(my_body) > len(snake["body"]):
        #   points[pos["index"]] += HEADWINFACTOR
        #   break

        # else:
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
  global grid, areas, AREAFACTOR
  

  food = data["board"]["food"]

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

  if data["turn"] >5:
    AREAFACTOR = 5

  for i in range(WIDTH+2):
    tmp = []
    for j in range(HEIGHT+2):
      tmp.append(0)
    grid.append(tmp)

  
  closest_food = {}
  is_there_food = 1
  if(len(data["board"]["food"]) > 0):
    closest_food = data["board"]["food"][0]
    for f in data["board"]["food"]:
      if(Distance_between(my_head, f) < Distance_between(my_head, closest_food)):
        closest_food = f
  else:
    is_there_food = 0

  
  ''''
  Dist_to_food = []
  for j in range(len(food)):
    Dist = Distance_between(my_head,food[j])
    Dist_to_food.append((Dist,j,food[j]))
  Dist_to_food.sort()
 '''
  
  areas = []
  # print(HEIGHT, WIDTH)
  grid_generation()
  for m in moves:
    area_check(index[m])
    death_check(index[m], data["you"]["id"])
    if(is_there_food):
      food_check(index[m], closest_food)
    
    head_check(index[m],data["you"]["id"])
    
    if len(my_body)>SHIFTLENGTH and data["you"]["health"]>SHIFTHEALTH:
      # print('called')
      move_to_perimeter(index[m])
    else:
      free_space(index[m],data["you"]["id"])


  move = ""
  max = -1000000
  ind = 0
  print("turn", data["turn"], points)
  for i in range(4):
    if(points[i]>max):
      max = points[i]
      ind = i
  
  move = moves[ind]

  return move

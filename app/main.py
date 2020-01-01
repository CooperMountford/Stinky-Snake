import json
import os
import random
import operator
import bottle
import math
import numpy as np
from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return
    '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
       Code by Cooper Mountford
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.
    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():

    data = bottle.request.json

    # Color fliping code to visually see that the snake is loading each run
    flip = random.randint(0, 1)
    if (flip == 0):
        color = "#101ade"
    else:
        color = "#f016c0"

    return {
        "color": color,
	    'headType': "fang",
	    "tailType": "hook"
    }

@bottle.post('/move')


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Deleted a test equal method. Not sure what I'd need it

    def pointString(self):
        return str(self.x) + ', ' + str(self.y)

    def display(self):
        return self.pointString()

    def closest(self, list):
        closest = list[0]
        for point in list:
            if (self.distance(point) < self.distance(closest)):
                closest = point
        return closest

    def distance(self, other): #
        return abs(self.x - other.x) + abs(self.y - other.y)

    # Not sure if I really need these
    def get(self, direction):
        if(direction == 'left'):
            return self.left()
        if(direction == 'right'):
            return self.right()
        if(direction == 'up'):
            return self.up()
        if(direction == 'down'):
            return self.down()


    def left(self):
        return(Point(self.x-1, self.y))

    def right(self):
        return(Point(self.x+1, self.y))

    def up(self):
        return(Point(self.x, self.y+1))

    def down(self):
        return(Point(self.x, self.y-1))

    def fourAround(self):
        # Movement options, clockwise from top (up)
        return [self.up(), self.right(), self.down(), self.left()]

    def eightAround(self):
        # Movement options, clockwise from top (up)
        return[self.up(), self.up().right(), self.right(), self.right().down(), self.down(), self.down().left(), self.left(), self.left().up()]

class Snake:
    def __init__(self, board, data):
        self.board = board
        self.id = data['id']
        self.health = data['health']
        self.head = Point(data['body'][0]['x'], data['body'][0]['y'])
        self.body = []
        self.head = Point(data['body'][-1]['x'], data['body'][-1]['y'])

        for tile in data['body']:
            self.body.append(tile)


        #and so on


        # Movement actions for snake to take and checks to see if actions are smart and/or deadly

class Board:
    def __init__(self, data):
        self.width = data['board']['width']
        self.height = data['board']['height']
        self.food = []
        self.snakes = []
        self.heads = []
        self.occupied = []
        self.me = data['you']['id']
        self.turn = data['turn']

        for food in data['board']['food']:
            self.food.append(Point(food['x'], food['y']))

        for snake in data['board']['snakes']:
            for tile in snake:
                self.occupied.append(Point(tile['x'], tile['y']))
            if(snake.id != self.me):
                self.snakes.append(snake)
                self.heads.append(snake.head)


        #and so on

    def visualize(self):
        # Prints a visual of the game board
        visual = np.matrix(self)
        print(visual)

        #TODO: Board print out is reflected and backwards for some reason and I can't figure it out
        #visual = np.rot90(visual)
        #visual = np.flip(visual, 0)
        #visual = np.flip(visual, 1)


    # TODO: Add methods about where things are and A* Pathing

def newMove():
    data = bottle.request.json

    board = Board(data)
    snake = board.player
    snake.choseMove()

    return{
        'move': snake.next_move,
        'taunt': 'Uh-Oh! Stinky!' # Not sure if taunt is still used or not. Theres nothing in the documentation about it at all
    }

def move():
    """
    TODO
    Track heads of other snakes to avoid head-to-head collisions
    Track sizes of other snakes

    Beginner:
    Tail-follow method seems best
    Trapping yourself is dangerous late game
    Head-to-heads are dangerous early and late game (mostly early)
    Size advantage is important beginning and late game
    Snakes really only starve if they don't work
    """
    data = bottle.request.json

    meId = data['you']['id']
    width = data['board']['width']
    board = [[' ' for i in range(width)] for j in range(width)]
    enemies = []
    heads = []

    snakes = data['board']['snakes']
    for snake in snakes:
        length = 1
        if(snake['id'] != meId):
            enemies.append(snake)
            heads.append(snake['body'][0]['x'])
            for i, tile in enumerate(snake['body']):
                if(i == 0):
                    board[tile['x']][tile['y']] = 'sh'
                    continue
                board[tile['x']][tile['y']] = 's'

        else:
            for i, tile in enumerate(snake['body']):
                #print('i: ' + str(i))
                #print('tile: ' + tile)
                if(i == 0):
                    board[tile['x']][tile['y']] = 'mh'
                    continue
                board[tile['x']][tile['y']] = 'm'

    # sh = enemy snake head
    # s = enemy snake body
    # mh = my head
    # m = my snake body

    #print(snakes)


    for food in data['board']['food']:
        board[food['x']][food['y']] = 'f'
        # square with food is f

    #TODO: Board print out is reflected and backwards for some reason and I can't figure it out
    #visual = np.rot90(visual)
    #visual = np.flip(visual, 0)
    #visual = np.flip(visual, 1)

    # Prints a visual of the game board
    visual = np.matrix(board)
    #print(visual)

    me = data['you']
    x = me['body'][0]['x']
    y = me['body'][0]['y']
    #print(me['health'])

    #0 = left, 1 = up, 2 = right, 3 = down
    priorityDirections = {
        "left": 0,
        "right": 0,
        "up": 0,
        "down": 0
    }

    distFoodLeft = []
    distFoodRight = []
    distFoodUp = []
    distFoodDown = []

    directions = ['up', 'down', 'left', 'right']
    direction = random.choice(directions)

    if(y+1 < width and board[x][y+1] != 'm' and board[x][y+1] != 'o' ):
        #print("chose down" + str(board[x][y+1]))
        priorityDirections["down"] += 1

        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x - food['x'])**2 + (y+1 - food['y'])**2 )
                distFoodDown.append(dist)

            priorityDirections["down"] += 100 - min(distFoodDown)
        #possibleDirections.append('down')
    if( x+1 < width and board[x+1][y] != 'm' and board[x+1][y] != 'o'):
        #print("chose right" + str(board[x+1][y]))
        #print("X+1 = " + str(x+1))
        priorityDirections["right"] += 1
        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x+1 - food['x'])**2 + (y - food['y'])**2 )
                distFoodRight.append(dist)

            priorityDirections["right"] += 100 - min(distFoodRight)
        #possibleDirections.append('right')
    if(x-1 >= 0 and board[x-1][y] != 'm' and board[x-1][y] != 'o'):
        #print("chose left" + str(board[x-1][y]))
        #possibleDirections.append('left')
        priorityDirections["left"] += 1
        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x-1 - food['x'])**2 + (y - food['y'])**2 )
                distFoodLeft.append(dist)
            priorityDirections["left"] += 100 - min(distFoodLeft)

    if(y-1 >= 0 and board[x][y-1] != 'm' and board[x][y-1] != 'o'):
        #print("went up")
        priorityDirections["up"] += 1
        if(data['you']['health'] < 50):
            for food in data['board']['food']:
                dist = math.sqrt( (x - food['x'])**2 + (y-1 - food['y'])**2 )
                distFoodUp.append(dist)
            #possibleDirections.append('up')

            priorityDirections["up"] += 100 - min(distFoodUp)



    #direction = random.choice(possibleDirections)
    direction = max(priorityDirections.iteritems(), key=operator.itemgetter(1))[0]

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )

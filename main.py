'''
Author: Kyle Yang
Creation Date: 4/22/22
Last Modified: 5/24/22
Project Description: This is a game where you have to avoid all of the obstacles
that are thrown at you like fireballs, cars, rockets, and cannons for 30 rounds.
There are 10 different types of obstacles including 5 different fireball colors,
2 different car and rocket sizes, and cannons with lots of animation and colors.
Instructions: Avoid the obstacles by pressing the arrow keys to move the player.
You can also collect the snowflakes on the screen to gain points for each round.
The player will have to survive for 30 rounds or gain 30 points to win the game.
Credits: Dad
Updates: Add new types of obstacles.
Rubric Items:
    Data Structures:
        List: Line 182
        Function: Line 275
        Class: Line 28
        Labels/Groups/Properties: Lines 32-57
    Animation: Lines 338-358
'''

from cmu_graphics import *

# constants
app.background = 'darkGray'
app.stepsPerSecond = 40

# classes
class GameState(object):
    '''
    Contains methods and properties for the game itself to run.
    '''
    def __init__(self):
        # Creates the properties, labels, and groups for the game state.
        self.mode = 'MENU'
        self.healthLabel = Label('Health:',200,390,visible=False,bold=True,fill='white')
        self.pointsLabel = Label('Points:',200,10,visible=False,bold=True,fill='white')
        self.roundsLabel = Label('Rounds:',200,200,fill='darkRed',size=30,visible=False,bold=True)
        self.pointsScored = Label('Points Scored:',200,140,visible=False,bold=True)
        self.roundsLasted = Label('Rounds Lasted:',200,160,visible=False,bold=True)
        self.highestScoreLabel = Label('Highest Score:',200,180,visible=False,bold=True)
        self.highestScore = 0
        self.highestRoundLabel = Label('Highest Round:',200,200,visible=False,bold=True)
        self.highestRound = 0
        self.winsLabel = Label('Wins:',200,220,visible=False,bold=True)
        self.wins = 0
        self.lossesLabel = Label('Losses:',200,240,visible=False,bold=True)
        self.losses = 0
        self.title = Label('Player Dodge Game',200,100,size=30,bold=True)
        self.start = Group(Rect(150,275,100,50),
                    Label('Start',200,300,fill='white',size=30,bold=True))
        self.again = Group(Rect(100,275,200,50),
                    Label('Play Again',200,300,fill='white',size=30,bold=True),visible=False)
        self.fireballs = Group()
        self.cars = Group()
        self.rockets = Group()
        self.cannons = Group()
        self.snowflakes = Group()
    
    def summonObstacle(self):
        # Summons a random obstacle based on the number of rounds.
        self.roundsLabel.visible = False
        random = randrange(1,self.rounds+1)
        if random <= 3:
            fireball = Fireball()
        if random == 4 or random == 8:
            car = Car()
        if random == 5 or random == 9:
            rocket = Rocket()
        if random == 6 or random >= 10:
            fireball = Fireball()
        if random == 7:
            cannon = Cannon()
        if random == randrange(1,self.rounds+1):
            snowflake = Snowflake()
        self.stepsPerObstacle = 0
        self.obstaclesSummoned += 1
    
    def nextRound(self):
        # Goes to the next round of the player dodge game.
        self.stepsPerObstacle = 0
        self.obstaclesSummoned = 0
        self.rounds += 1
        self.roundsLabel.value = 'Round ' + str(self.rounds)
        self.roundsLabel.size = 100
        self.roundsLabel.visible = True
        for cannon in self.cannons:
            cannon.body.visible = False
            cannon.ball.visible = False
            cannon.fire.visible = False
        self.fireballs.clear()
        self.cars.clear()
        self.rockets.clear()
        self.cannons.clear()
        self.snowflakes.clear()
    
    def showStats(self):
        # Shows your stats after you win or lose the game.
        self.mode = 'END'
        self.pointsLabel.visible = False
        self.healthLabel.visible = False
        app.player.drawing.visible = False
        self.title.visible = True
        self.start.visible = True
        self.again.visible = True
        self.pointsScored.value = 'Points Scored: ' + str(self.points)
        self.roundsLasted.value = 'Rounds Lasted: ' + str(self.rounds)
        self.pointsScored.visible = True
        self.roundsLasted.visible = True
        if self.points > self.highestScore:
            self.highestScore = self.points
        if self.rounds > self.highestRound:
            self.highestRound = self.rounds
        self.highestScoreLabel.value = 'Highest Score: ' + str(self.highestScore)
        self.highestScoreLabel.visible = True
        self.highestRoundLabel.value = 'Highest Round: ' + str(self.highestRound)
        self.highestRoundLabel.visible = True
        self.winsLabel.value = 'Wins: ' + str(self.wins)
        self.winsLabel.visible = True
        self.lossesLabel.value = 'Losses: ' + str(self.losses)
        self.lossesLabel.visible = True
        for cannon in self.cannons:
            cannon.body.visible = False
            cannon.ball.visible = False
            cannon.fire.visible = False
        self.fireballs.clear()
        self.cars.clear()
        self.rockets.clear()
        self.cannons.clear()
        self.snowflakes.clear()
        app.background = gradient('darkGray','pink','purple','indigo')
    
    def startGame(self):
        # Starts the player dodge game.
        self.rounds = 0
        self.stepsPerObstacle = 0
        self.obstaclesSummoned = 0
        self.points = 0
        self.pointsLabel.value = 'Points: ' + str(self.points)
        self.pointsLabel.visible = True
        self.health = 100
        self.healthLabel.value = 'Health: ' + str(self.health)
        self.healthLabel.visible = True
        app.player.drawing.centerX = 200
        app.player.drawing.centerY = 200
        app.player.drawing.visible = True
        self.title.visible = False
        self.start.visible = False
        self.again.visible = False
        self.pointsScored.visible = False
        self.roundsLasted.visible = False
        self.highestScoreLabel.visible = False
        self.highestRoundLabel.visible = False
        self.winsLabel.visible = False
        self.lossesLabel.visible = False
        app.background = gradient('darkGray','indigo')

class Player(object):
    '''
    Contains properties for the player object that is called.
    '''
    def __init__(self):
        # Creates properties for the player.
        self.drawing = Group(Circle(200,200,25),
            Circle(200,200,20,fill='white'),
            Line(200,225,200,275,lineWidth=5),
            Line(175,250,200,225,lineWidth=5),
            Line(225,250,200,225,lineWidth=5),
            Line(200,275,175,300,lineWidth=5),
            Line(200,275,225,300,lineWidth=5),
            Circle(190,200,5),
            Circle(210,200,5))
        self.drawing.visible = False
        self.drawing.height /= 2
        self.drawing.width /= 2

class Fireball(object):
    '''
    Contains properties for each fireball object that is called.
    '''
    def __init__(self):
        # Creates properties for the fireball.
        self.colors = ['red','orange','yellow','green','blue']
        self.drawing = Star(randrange(60,340),-20,15,50)
        self.drawing.angle = angleTo(self.drawing.centerX,self.drawing.centerY,app.player.drawing.centerX,app.player.drawing.centerY)
        if app.game.rounds == 1:
            self.drawing.speed = randrange(1,2)
        elif app.game.rounds == 2:
            self.drawing.speed = randrange(1,3)
        elif 2 < app.game.rounds < 6:
            self.drawing.speed = randrange(1,4)
        elif 5 < app.game.rounds < 10:
            self.drawing.speed = randrange(1,5)
        else:
            self.drawing.speed = randrange(1,6)
        self.drawing.fill = self.colors[self.drawing.speed-1]
        app.game.fireballs.add(self.drawing)

class Car(object):
    '''
    Contains properties for each car object that is called.
    '''
    def __init__(self):
        # Creates properties for the car.
        self.drawing = Group(Polygon(25,125,75,75,125,75,175,125,fill='blue'),
                Rect(25,125,200,50,fill='orange'),
                Rect(75,80,50,40),
                Circle(75,175,25,fill='lightGray',border='gray',borderWidth=10),
                Circle(175,175,25,fill='lightGray',border='gray',borderWidth=10))
        if app.game.rounds < 8:
            self.drawing.height /= 4
            self.drawing.width /= 4
        else:
            if randrange(0,2) == 0:
                self.drawing.height /= 3
                self.drawing.width /= 3
            else:
                self.drawing.height /= 4
                self.drawing.width /= 4
        self.drawing.centerX = -50
        self.drawing.centerY = randrange(60,340)
        app.game.cars.add(self.drawing)

class Rocket(object):
    '''
    Contains properties for each rocket object that is called.
    '''
    def __init__(self):
        # Creates properties for the rocket.
        self.drawing = Group(RegularPolygon(200,200,30,3,fill='violet',border='black'),
                    Rect(180,215,40,150,fill='gray',border='black'),
                    Polygon(180,300,180,250,150,300,fill='violet',border='black'),
                    Polygon(220,300,220,250,250,300,fill='violet',border='black'),
                    Polygon(180,365,220,365,220,405,200,385,180,405,fill=gradient('yellow','red')))
        if app.game.rounds < 9:
            self.drawing.height /= 4
            self.drawing.width /= 4
        else:
            if randrange(0,2) == 0:
                self.drawing.height /= 3
                self.drawing.width /= 3
            else:
                self.drawing.height /= 4
                self.drawing.width /= 4
        self.drawing.centerY = 460
        self.drawing.centerX = randrange(60,340)
        app.game.rockets.add(self.drawing)

class Cannon(object):
    '''
    Contains properties for each cannon object that is called.
    '''
    def __init__(self):
        # Creates properties for the cannon.
        self.drawing = Circle(10,220,10,fill='brown')
        self.drawing.body = Group(Oval(20,200,50,30),
                    Oval(40,200,10,30))
        self.drawing.ball = Circle(50,0,15,fill=gradient('white','black','black'),visible=False)
        self.drawing.fire = Polygon(40,170,60,170,55,180,60,190,40,190,fill=gradient('yellow','red'),visible=False)
        self.drawing.centerX = -40
        self.drawing.body.centerX = -30
        self.drawing.centerY = randrange(60,340) + 10
        self.drawing.body.centerY = self.drawing.centerY - 20
        self.drawing.energy = 0
        app.game.cannons.add(self.drawing)

class Snowflake(object):
    '''
    Contains properties for each snowflake object that is called.
    '''
    def __init__(self):
        # Creates properties for the snowflake.
        self.drawing = Star(randrange(60,340),randrange(60,340),10,10,fill='white')
        app.game.snowflakes.add(self.drawing)

def main():
    # This function creates the objects for the game and player.
    app.game = GameState()
    app.player = Player()

main()

def onKeyHold(keys):
    # This function is called every time you hold a key.
    if ('up' in keys) and app.player.drawing.centerY > 60:
        app.player.drawing.centerY -= 10
    if ('down' in keys) and app.player.drawing.centerY < 340:
        app.player.drawing.centerY += 10
    if ('left' in keys) and app.player.drawing.centerX > 60:
        app.player.drawing.centerX -= 10
    if ('right' in keys) and app.player.drawing.centerX < 340:
        app.player.drawing.centerX += 10

def onStep():
    # This function is called for 40 times in a second.
    if app.game.mode == 'START':    
        if app.game.stepsPerObstacle == 50 - app.game.rounds and app.game.obstaclesSummoned != app.game.rounds:
            app.game.summonObstacle()
        if app.game.stepsPerObstacle == 300 - app.game.rounds:
            if app.game.rounds >= 30:
                app.game.title.value = 'You Win!'
                app.game.wins += 1
                app.game.showStats()
            else:
                app.game.nextRound()
        if app.game.roundsLabel.size != 30:
            app.game.roundsLabel.size -= 10
        if app.game.health <= 0:
            app.game.title.value = 'Game Over!'
            app.game.losses += 1
            app.game.showStats()
        if app.game.points >= 30:
            app.game.title.value = 'You Win!'
            app.game.wins += 1
            app.game.showStats()
        app.game.healthLabel.value = 'Health: ' + str(app.game.health)
        for fireball in app.game.fireballs:
            fireball.centerX, fireball.centerY = getPointInDir(fireball.centerX,fireball.centerY,fireball.angle,fireball.speed*2)
            if fireball.hitsShape(app.player.drawing):
                app.game.health -= 10
                app.game.fireballs.remove(fireball)
            if fireball.top >= 400:
                app.game.fireballs.remove(fireball)
        for car in app.game.cars:
            car.centerX += 5
            if car.hitsShape(app.player.drawing):
                app.game.health -= 10
                app.game.cars.remove(car)
            if car.left >= 400:
                app.game.cars.remove(car)
        for rocket in app.game.rockets:
            rocket.centerY -= 5
            if rocket.hitsShape(app.player.drawing):
                app.game.health -= 10
                app.game.rockets.remove(rocket)
            if rocket.bottom <= 0:
                app.game.rockets.remove(rocket)
        for cannon in app.game.cannons:
            if cannon.energy >= 50:
                cannon.centerX -= 1
                cannon.body.centerX -= 1
                cannon.ball.centerX += 10
                cannon.fire.visible = False
                if cannon.ball.hitsShape(app.player.drawing):
                    app.game.health -= 10
                    cannon.ball.left = 400
                if cannon.body.right <= 0:
                    cannon.visible = False
                    cannon.body.visible = False
                    cannon.ball.visible = False
            if cannon.energy == 50:
                cannon.ball.visible = True
                cannon.fire.visible = True
                cannon.ball.centerY = cannon.body.centerY
                cannon.fire.centerY = cannon.body.centerY
            if cannon.energy <= 50:
                cannon.centerX += 1
                cannon.body.centerX += 1
            cannon.energy += 1
        for snowflake in app.game.snowflakes:
            if snowflake.hitsShape(app.player.drawing):
                app.game.points += 1
                app.game.snowflakes.remove(snowflake)
        app.game.pointsLabel.value = 'Points: ' + str(app.game.points)
        app.game.stepsPerObstacle += 1

def onMousePress(mouseX,mouseY):
    # This function is called every time you left click somewhere.
    if app.game.start.hits(mouseX,mouseY) and app.game.mode == 'MENU' or app.game.again.hits(mouseX,mouseY) and app.game.mode == 'END':
        app.game.mode = 'START'
        app.game.startGame()


cmu_graphics.run()

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import turtle
from random import randint
import time
H = 440
W = 440
M = 30
TOLERATE = 5

class SnakeEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self, env_info={'state_space':None}):
		# background
		self.win = turtle.Screen()
		self.win.bgcolor('black')
		self.win.setup(width = W, height = H)
		self.win.tracer(0)

		# snake
		self.snake = turtle.Turtle()
		self.snake.shape('square')
		self.snake.speed(0)
		self.snake.penup()
		self.snake.color('white')
		self.snake.shapesize(0.5, 0.5)
		self.snake.goto(0,0)
		self.body = []
		self.body.append(self.snake)
		self.speed = 200

		# berry
		self.berry = turtle.Turtle()
		self.berry.shape('circle')
		self.berry.speed(0)
		self.berry.penup()
		self.berry.color('lightgreen')
		self.berry.shapesize(0.2, 0.2)
		self.generate_food()

		# score
		self.total = 0
		self.best = 0

		self.score = turtle.Turtle()
		self.score.speed(0)
		self.score.color('white')
		self.score.penup()
		self.score.hideturtle()
		self.score.goto(0,(H/2)-M)
		self.score.write("Score: {0}  Best: {1}".format(self.total,self.best),align='center', font=('Courier', 8, 'normal'))

		## controls
		self.win.listen()
		# arrow keys
		self.win.onkey(self.move_left, 'Left')
		self.win.onkey(self.move_right, 'Right')
		self.win.onkey(self.move_up, 'Up')
		self.win.onkey(self.move_down, 'Down')
		# a,s,d,w
		self.win.onkey(self.move_left, 'A')
		self.win.onkey(self.move_right, 'D')
		self.win.onkey(self.move_up, 'W')
		self.win.onkey(self.move_down, 'S')

		self.direction = 'stop'
		self.prev_direction = 'stop'
		self.last_key = 'del'
		self.cur_key = 'del'

		self.seed()
		self.done = False
		self.reward = 0
		self.action_space = 4
		self.state_space = 12
		self.env_info = env_info

	def generate_food(self):
		while True:
			x = randint(-((W-M)//2),(W-M)//2)
			y = randint(-((H-M)//2),(H-M)//2)
			if self.check_on_walls(x,y) and self.check_on_body(x,y):
				break
		self.berry.goto(x,y)

	def check_on_walls(self,x,y):
		if x <= (-(W//2-M)): return False
		if x >= (W//2-M): return False
		if y <= (-(H//2-M)): return False
		if y >= (H//2-M): return False
		return True

	def check_on_body(self,x,y):
		for i in range(0,len(self.body)-1):
			snake_x = self.body[i].xcor()
			snake_y = self.body[i].ycor()
			if (snake_x - TOLERATE) <= x <= (snake_x + TOLERATE): return False
			if (snake_y - TOLERATE) <= y <= (snake_y + TOLERATE): return False
		# if x == (self.snake.xcor()): return False
		# if y == (self.snake.ycor()): return False		
		return True

	def move(self):
		if self.direction == 'left':
			x = self.snake.xcor()			
			self.snake.setx(x - 10)
		if self.direction == 'right':
			x = self.snake.xcor()			
			self.snake.setx(x + 10)
		if self.direction == 'up':
			y = self.snake.ycor()			
			self.snake.sety(y + 10)
		if self.direction == 'down':
			y = self.snake.ycor()			
			self.snake.sety(y - 10)
		# if len(self.body) == 1:
		# 	x = self.snake.xcor()
		# 	y = self.snake.ycor() 
		# 	self.body[0].goto(x,y)
		for i in range(len(self.body)-1,0,-1):
			x = self.body[i-1].xcor()
			y = self.body[i-1].ycor()
			self.body[i].goto(x,y)

	def move_left(self):
		self.last_key = self.cur_key
		self.cur_key = 'left'
		if self.direction != 'right':
			self.direction = 'left'

	def move_right(self):
		self.last_key = self.cur_key
		self.cur_key = 'right'
		if self.direction != 'left':
			self.direction = 'right'

	def move_up(self):
		self.last_key = self.cur_key
		self.cur_key = 'up'
		if self.direction != 'down':
			self.direction = 'up'

	def move_down(self):
		self.last_key = self.cur_key
		self.cur_key = 'down'
		if self.direction != 'up':
			self.direction = 'down'

	def eat_berry(self):
		x = self.snake.xcor()
		y = self.snake.ycor()
		segment = turtle.Turtle()
		segment.shape('square')
		segment.speed(0)
		segment.penup()
		segment.color('white')
		segment.shapesize(0.5, 0.5)
		segment.goto(x,y)
		self.body.append(segment)

	def collision_on_body(self):
		if len(self.body)>2:
			x = self.body[0].xcor()
			y = self.body[0].ycor()
			for i in range(2, len(self.body)):
				if self.body[i].xcor() == x and self.body[i].ycor() == y:
					self.game_over()
					self.reset_map()
					self.reset_score()
					break


	def move_body_to_wall(self):
		for i in range(0,len(self.body)):
			x = self.body[i].xcor()
			y = self.body[i].ycor()
			if x > (W//2)-M:
				self.body[i].goto(-(W//2)+M,y)
			if x < -(W//2)+M:
				self.body[i].goto((W//2)-M,y)
			if y > (H//2)-M:
				self.body[i].goto(x,-(H//2)+M)
			if y < -(H//2)+M:
				self.body[i].goto(x,(H//2)-M)

	def reset_map(self):
		score = self.total
		best = self.best
		turtle.clearscreen()
		self.__init__()
		self.total = score
		self.best = best

	def game_over(self):
		self.reward -= 50
		game_over = turtle.Turtle()
		game_over.speed(0)
		game_over.color('white')
		game_over.penup()
		game_over.hideturtle()
		game_over.goto(0,0)
		game_over.write("GAME OVER!! \nScore: {0}  Best: {1}".format(self.total,self.best),align='center', font=('Courier', 12, 'normal'))
		time.sleep(1)
		game_over.hideturtle()
		game_over.goto(1000,1000)
		game_over.clear()

	def reset_score(self):
		if(self.total>self.best):
			self.best = self.total
			self.reward += 10
		self.total = 0
		self.update_score()

	def update_score(self):
		self.score.clear()
		self.score.write("Score: {0}  Best: {1}".format(self.total,self.best),align='center', font=('Courier', 8, 'normal'))

	def run_game(self):
		self.win.update()	
			
		if self.cur_key == self.last_key and self.cur_key != 'del':
			if self.speed > 120:
				self.speed -= 20
			elif self.speed > 80:
				self.speed -= 5
			elif self.speed <= 50 :
				self.speed = 200
		else:
			self.speed = 200

		self.move_body_to_wall()	
		self.move()	
		self.collision_on_body()
		if (self.berry.xcor() - TOLERATE) <= self.body[0].xcor() <= (self.berry.xcor() + TOLERATE) and (self.berry.ycor() - TOLERATE) <= self.body[0].ycor() <= (self.berry.ycor() + TOLERATE):
			self.eat_berry()
			self.generate_food()
			self.total += 10
			self.reward += 10
			self.update_score()
		print(self.reward)
	
	#### Environment Functions ####
	def seed(self, seed=None):
		self.np_random, seed = seeding.np_random(seed)
		return [seed]

	def reset(self):
		self.reset_map()
		self.reset_score()
		self.done = False

		state = self.get_state()

		return state

	def step(self, action):
		'''
		Action:

		0: Up
		1: Down
		2: Left
		3: Right

		'''
		if action == 0: 
			self.move_up()
		if action == 1:
			self.move_down()
		if action == 2:
			self.move_left()
		if action == 3:
			self.move_right()

		self.run_game()
		state = self.get_state()
		return state, self.reward, self.done,{}

	def get_state(self):
		# snake coordinate abs
		x = self.snake.xcor()/(W-M*2)
		y = self.snake.ycor()/(H-M*2)

		# snake coordinates scaled 0-1
		xs = x/(W-M*2+0.5)
		ys = y/(H-M*2+0.5)

		# berry corrdinate abs
		bx = self.berr.xcor()/(W-M*2)
		by = self.berr.ycor()/(Y-M*2)

		# berry coordinates scaled 0-1
		bxs = bx/(W-M*2+0.5)
		bys = by/(H-M*2+0.5)

		# body close
		body_up = []
		body_down = []
		body_left = []
		body_right = []

		if len(self.body) > 3:
			for i in range(3, len(self.body)):
				if self.body[i].distance(self.snake) == 10:
					if self.body[i].ycor() < self.snake.ycor():
						body_down.append(1)
					elif self.body[i].ycor() > self.snake.ycor():
						body_up.append(1)
					if self.body[i].xcor() < self.snake.xcor():
						body_left.append(1)
					elif self.body[i].xcor() > self.snake.xcor():
						body_right.append(1)

		if len(body_up)>0: 
			body_up=1 
		else: 
			body_up=0
		if len(body_down)>0: 
			body_down=1 
		else: 
			body_down=0
		if len(body_left)>0: 
			body_left=1 
		else: 
			body_left=0
		if len(body_right)>0: 
			body_right=1 
		else: 
			body_right=0


		## state shape will be:
		## bxs,bys,xs,ys,body_up,body_down,body_left,body_right,direction_up,direction_down,direction_left,direction_right
		if self.env_info['state_space'] == 'coordinates':
			state = [bxs,bys,xs,ys,int(body_up),int(body_down),int(body_left),int(body_right),int(self.direction=='up'), int(self.direction == 'down'), int(self.direction == 'left'), int(self.direction=='right')]
		elif self.env_info['state_space'] == 'no direction':
			state = [int(y<by), int(x<bx), int(y>by), int(x>bx),int(body_up),int(body_down),int(body_left),int(body_right),0,0,0,0 ]
		elif self.env_info['state_space'] == 'no body knowledge':
			state = [int(y<by), int(x<bx), int(y>by), int(x>bx),0,0,0,0,int(self.direction=='up'), int(self.direction == 'down'), int(self.direction == 'left'), int(self.direction=='right')]
		else:
			state = [int(y<by), int(x<bx), int(y>by), int(x>bx),int(body_up),int(body_down),int(body_left),int(body_right),int(self.direction=='up'), int(self.direction == 'down'), int(self.direction == 'left'), int(self.direction=='right')]

		return state



if __name__ == '__main__':
	env = Snake()
	while True:
		env.run_game()
		time.sleep(env.speed/1000)



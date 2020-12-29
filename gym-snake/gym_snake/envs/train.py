from snake_env import SnakeEnv

import random
import numpy as np
import time
import matplotlib.pyplot as plt
from collections import deque
import tensorflow as tf

from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class DQN:
	''' Deep Q Network '''

	def __init__(self, env, params):

		self.action_space = env.action_space
		self.state_space = env.state_space
		self.epsilon = params['epsilon']
		self.gamma = params['gamma']
		self.batch_size = params['batch_size']
		self.epsilon_min = params['epsilon_min']
		self.epsilon_decay = params['epsilon_decay']
		self.learning_rate = params['learning_rate']
		self.memory = deque(maxlen=2500)
		self.model = self.build_model()


	def build_model(self):
		model = Sequential()
		model.add(Dense(128, input_shape=(self.state_space,), activation='relu'))
		model.add(Dense(128, activation='relu'))
		model.add(Dense(128, activation='relu'))
		model.add(Dense(128, activation='relu'))
		model.add(Dense(self.action_space, activation='softmax'))
		model.compile(loss='mse',optimizer=Adam(lr=self.learning_rate))
		return model

	def remember(self, state, action, reward, next_state, done):
		self.memory.append((state, action, reward, next_state, done))

	def act(self, state):
		if np.random.random <= self.epsilon:
			return random.randrange(self.action_space)
		act_values = self.model.predict(state)
		return np.argmax(act_values[0])

	def replay(self):
		if len(self.memory) < self.batch_size:
			return

		minibatch = random.sample(self.memory, self.batch_size)
		states = np.array([i[0] for i in minibatch])
		actions = np.array([i[1] for i in minibatch])
		rewards = np.array([i[2] for i in minibatch])
		next_states = np.array([i[3] for i in minibatch])
		dones = np.array([i[4] for i in minibatch])

		states = np.squeeze(states)
		next_states = np.squeeze(next_states)

		targets = rewards + self.gamma*(np.argmax(self.model.predict_on_batch(next_states), axis=1))*(1-dones)
		targets_full = self.model.predict_on_batch(states)

		ind = np.array([i for i in range(self.batch_size)])
		targets_full[[ind],[actions]] = targets

		self.model.fit(states, targets_full, epochs = 1)

		if self.epsilon > self.epsilon_min:
			self.epsilon *= self.epsilon_decay

	def train_dqn(episode, env):

		sum_of_rewards = []
		agent = DQN(env, params)
		for e in range(episode):
			state = env.reset()
			state = np.reshape(state, (1, env.state_space))
			score = 0
			max_steps = 10000
			for i in range(max_steps):
				action = agent.act(state)
				prev_state = state
				next_state, reward, done, _ = env.step(action)
				score += reward
				next_state = np.reshape(next_state,(1, env.state_space))
				agent.remember(state,action,reward,next_state,done)
				state = next_state
				if params['batch_size'] > 1:
					agent.replay()
				if done:
					print(f'final state before dying: {str(prev_state)}')
					print(f'episode: {e+1}/{episode}, score:{score}')
					break
			sum_of_rewards.append(score)
		return sum_of_rewards

if __name__ == '__main__':

	params = dict()
	params['name'] = None
	params['epsilon'] = 1
	params['gamma'] = .95
	params['batch_size'] = 500
	params['epsilon_min'] = .01
	params['epsilon_decay']=.995
	params['learning_rate']=0.00025

	results = dict()
	ep = 50

	env_infos = {'States: only walls':{'state_space':'no body knowledge'}, 'States: direction 0 or 1':{'state_space':''}, 'States: coordinates': {'state_space':'coordinates'}, 'States: no direction':{'state_space':'no direction'}}

	env = SnakeEnv()

	sum_of_rewards = train_dqn(ep, env)
	results[params['name']] = sum_of_rewards
	print(results)
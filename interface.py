# coding=utf-8
from multiprocessing.managers import BaseManager
import threading
import random

import config

class Interface(object):
	def __init__(self, interface_id):
		BaseManager.register('Game2Agent')
		BaseManager.register('Agent2Game')
		manager = BaseManager(address=(config.server, config.server_port + interface_id - 1), authkey='dqn')
		manager.connect()

		self.g2a = manager.Game2Agent()
		self.a2g = manager.Agent2Game()
		print("interface_id is {}, port is {}".format(interface_id, config.server_port + interface_id - 1))

	# Lua Interface
	def ReceiveAction(self):
		# action = self.a2g.get()
		# print action
		# return action
		try:
			action = self.a2g.get()
			# action = self.a2g.get(block=False)
			# action = random.randint(1,19)
			# print action
			return action
		except: 
			return -1

	def SendSample(self, state, action, reward, next, done):
		self.g2a.put([state, action, reward, next, done])

def LuaTable2List(lua_table):

	if not lua_table or type(lua_table) == list:
		return lua_table
	else:
		return [float(lua_table[x+1]) for x in range(len(lua_table))] 

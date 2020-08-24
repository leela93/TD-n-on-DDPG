# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 17:08:55 2020
@author: leela
"""
import numpy as np
import torch
#from collections import deque
import torch.nn as nn
import torch.nn.functional as F
#import random
#import time
class MemoryBuffer:

    def __init__(self, size):
                    self.buffer = []
                    self.maxSize = size
                    self.len = 0

    def sample(self, batch_size):

        """
        samples a random batch from the replay memory buffer
        :param count: batch size
        :return: batch (numpy array)
        """
        ind = np.random.randint(0, len(self.buffer), size = batch_size)
        batch_states, batch_plc, batch_action, batch_reward, batch_next_state, batch_done = [], [], [],[], [], []
        for i in ind:
            state, plc, action, reward, next_state, done = self.buffer[i]
            batch_states.append(np.array(state, copy = False))
            batch_plc.append(np.array(plc, copy = False))
            batch_action.append(np.array(action, copy = False))
            batch_reward.append(np.array(reward, copy = False))
            batch_next_state.append(np.array(next_state, copy = False))
            batch_done.append(np.array(done, copy = False))
        return np.array(batch_states), np.array(batch_plc), np.array(batch_action), np.array(batch_reward), np.array(batch_next_state), np.array(batch_done)

    def len(self):
        return self.len

    def add(self, s,d, a, r, s1, done):
        """
        adds a particular transaction in the memory buffer
        :param s: current state
        :param d: desired action
        :param a: action taken
        :param r: reward received
        :param s1: next state
        :return:
        """
        transition = (s,d,a,r,s1,done)
        if len(self.buffer) == self.maxSize:
            self.buffer[int(self.len)] = transition
            self.len = (self.len + 1) % self.maxSize
        else:
            self.buffer.append(transition)

    def clearmemory(self):
         self.buffer.clear()
         self.len = 0

EPS = 0.003

def fanin_init(layer):
    fanin = layer.weight.data.size()[0]
    v = 1. / np.sqrt(fanin)
    return (-v,v)

class Critic(nn.Module):

    def __init__(self, state_dim, action_dim,neurons):
        """
        :param state_dim: Dimension of input state (int)
        :param action_dim: Dimension of input action (int)
        :return:
        """
        super(Critic, self).__init__()

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.h_neurons = neurons

        self.fcs1 = nn.Linear(state_dim,self.h_neurons) #previous:7
        #self.fcs1_bn = nn.BatchNorm1d(10)
        self.fcs1.weight.data.uniform_(*fanin_init(self.fcs1))

        self.fcs2 = nn.Linear(self.h_neurons,self.h_neurons) #(7,12)
        self.fcs2.weight.data.uniform_(*fanin_init(self.fcs2))
        self.fca1 = nn.Linear(action_dim,self.h_neurons) #(12)

        self.fc2 = nn.Linear(40,self.h_neurons) #(24,8)
        self.fc2.weight.data.uniform_(*fanin_init(self.fc2))
        self.fc3 = nn.Linear(self.h_neurons,self.h_neurons) #(8,1)
        self.fc3.weight.data.uniform_(*fanin_init(self.fc3))
        self.fc4 = nn.Linear(self.h_neurons,1)
        self.fc4.weight.data.uniform_(-3e-3, 3e-3)
        #self.reset_parameters()

    def reset_parameters(self):
        self.fcs1.weight.data.uniform_(*fanin_init(self.fcs1))
        self.fcs2.weight.data.uniform_(*fanin_init(self.fcs2))
        self.fc2.weight.data.uniform_(*fanin_init(self.fc2))
        self.fc3.weight.data.uniform_(*fanin_init(self.fc3))
        self.fc4.weight.data.uniform_(-3e-3, 3e-3)

    def forward(self, state, action):
        """
        returns Value function Q(s,a) obtained from critic network
        :param state: Input state (Torch Variable : [n,state_dim] )
        :param action: Input Action (Torch Variable : [n,action_dim] )
        :return: Value function : Q(S,a) (Torch Variable : [n,1] )
        """
        ##print("\nsstate in before fwd",state.size(),"action in before fwd",action.size())
        s1 = F.relu((self.fcs1(state)))
        s2 = F.relu(self.fcs2(s1))
        a1 = F.relu(self.fca1(action))
        #print("action",a1.shape)
        #print("state",s2.shape)
        x = torch.cat((s2,a1),dim=1)
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x


class Actor(nn.Module):

    def __init__(self, state_dim, action_dim, neurons): #, action_lim
        """
        :param state_dim: Dimension of input state (int)
        :param action_dim: Dimension of output action (int)
        :param action_lim: Used to limit action in [-action_lim,action_lim]
        :return:
        """
        super(Actor, self).__init__()

        self.state_dim = state_dim
        self.action_dim = action_dim
        self.h_neurons = neurons
        #self.check = torch.ones(32,1)

        self.fc1 = nn.Linear(state_dim,self.h_neurons)#(7)
        self.fc1.weight.data.uniform_(*fanin_init(self.fc1))
        self.fc2 = nn.Linear(self.h_neurons,self.h_neurons) #(7,12)
        self.fc2.weight.data.uniform_(*fanin_init(self.fc2))
        self.fc3 = nn.Linear(self.h_neurons,self.h_neurons) #(12,5)
        self.fc3.weight.data.uniform_(*fanin_init(self.fc3))
        self.fc4 = nn.Linear(self.h_neurons,action_dim) #(5)
        self.fc4.weight.data.uniform_(-3e-3,3e-3)
        #self.reset_parameters()

    def reset_parameters(self):
        self.fc1.weight.data.uniform_(*fanin_init(self.fc1))
        self.fc2.weight.data.uniform_(*fanin_init(self.fc2))
        self.fc3.weight.data.uniform_(*fanin_init(self.fc3))
        self.fc4.weight.data.uniform_(-3e-3,3e-3)



    def forward(self, state):
        """
        returns policy function Pi(s) obtained from actor network
        this function is a gaussian prob distribution for all actions
        with mean lying in (-1,1) and sigma lying in (0,1)
        The sampled action can , then later be rescaled
        :param state: Input state (Torch Variable : [n,state_dim] )
        :return: Output action (Torch Variable: [n,action_dim] )
        """
        #x = state
        x1 = F.relu((self.fc1(state)))
        #print("state",state.shape)
        x2 = F.relu(self.fc2(x1))
        x3 = F.relu(self.fc3(x2))
        action = F.relu(self.fc4(x3))
        m = nn.Tanh()
        action = m(action)

        return action


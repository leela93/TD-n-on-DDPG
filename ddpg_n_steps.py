# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:35:51 2020
@author: leela
"""
from __future__ import division
import torch
import gc
import numpy as np
from random import randrange
import datetime
import torch.nn as nn
import shutil
from Environment import bulk_good
from plc import plc
from actor_critic_memory import MemoryBuffer, Actor, Critic
import os
import time

class OrnsteinUhlenbeckActionNoise:
    def __init__(self,action_dim, mu=0, theta=0.15, sigma=0.2):
        self.action_dim = action_dim
        self.mu = mu
        self.theta = theta
        self.sigma = sigma
        self.x = np.ones(self.action_dim)*self.mu
    
    def reset(self):
        self.x = np.ones(self.action_dim)*self.mu
    
    def sample(self):
        dx = self.theta * (self.mu - self.x)
        dx = dx + self.sigma*np.random.randn(len(self.x))
        self.x = self.x + dx
        return self.x

def soft_update(target, source, tau):
    
    for target_param, param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(
                target_param.data*(1.0-tau)+param.data*tau)
        
def hard_update(target, source):
    
    for target_param, param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(param.data)

def save_training_checkpoint(state, is_best, episode_count):
    
    filename = str(episode_count)+'checkpoint.path.rar'
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'model_best.pth.tar')
    
    
class Trainer:
    def __init__(self, state_dim, action_dim,mse, ram, batch_size,actor_neurons,critic_neurons):
        """
        :state_dim: Dimensions of state
        :action_dim: Dimesions of action
        :ram: replay memory buffer 
        :batch_size: Size of batch
        """
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.batch_size = batch_size
        self.ram = ram
        self.noise =OrnsteinUhlenbeckActionNoise(self.action_dim)
        self.learning_actor = 0.0001
        self.learning_critic = 0.001
        self.gamma = 0.99
        self.tau = 0.001
        self.mse = nn.MSELoss()
        self.l_loss = nn.L1Loss()
        self.lambda_mse = mse
        self.neurons_a = actor_neurons
        self.neurons_c = critic_neurons
        self.actor = Actor(self.state_dim, self.action_dim,self.neurons_a)
        self.target_actor = Actor(self.state_dim, self.action_dim,self.neurons_a)
        self.target_actor.load_state_dict(self.actor.state_dict())
        self.actor_optimizer = torch.optim.Adam(self.actor.parameters(), self.learning_actor)
        
        self.critic = Critic(self.state_dim, self.action_dim,self.neurons_c)
        self.target_critic = Critic(self.state_dim, self.action_dim,self.neurons_c)
        self.target_critic.load_state_dict(self.critic.state_dict())
        self.critic_optimizer = torch.optim.Adam(self.critic.parameters(), self.learning_critic)
        
        hard_update(self.target_actor, self.actor)
        hard_update(self.target_critic, self.critic)
        
        self.loss_l1_list = []
        self.loss_mse_list = []
        self.loss_final_list = []
        self.mse_logic = []
        self.actor_logic = []
        self.check = torch.ones(32,1)
    def optimize(self,s,max_steps,td_n):
        """
        Samples a random batch from replay memory and performs optimization
        """
        
        s1, d1, a1, r1, s2, done = self.ram.sample(self.batch_size)
        s1 = torch.from_numpy(s1).float()
        #print(s1.shape)
        d1 = torch.from_numpy(d1).float()
        d1 = d1.unsqueeze(1)
        d1.requires_grad = True
        d1_copy = d1.detach().cpu().numpy()
        self.mse_logic.append(d1_copy[-1][-1])
        a1 = torch.from_numpy(a1).float()
        #print(a1.shape)
        r1 = torch.from_numpy(r1).float()
        r1 = torch.squeeze(r1)
        #print(r1.size())
        s2 = torch.from_numpy(s2).float()
        done = torch.from_numpy(done).float()
        self.t = s
        self.T = max_steps
        self.td_n = td_n
        self.td_tau = self.t-self.td_n+1
        if self.td_tau >= 0:
            for i in range(self.td_tau+1, min(self.td_tau+self.td_n, self.T)):
                self.G =  self.gamma**(i-self.td_tau-1)*(r1)
                if self.td_tau+self.td_n < self.T:
            #-----------optimize critic -----------------------------------
                    a2 = self.target_actor.forward(s2).detach()
                    noise = a1.data.normal_(0,0.2)
                    noise = noise.clamp(-0.5,0.5)
                    a2 = (a2+noise).clamp(-1,1)
                    next_val = torch.squeeze(self.target_critic.forward(s2,a2).detach())
                    y_expected = self.G + self.gamma**(self.td_n)*next_val*(1-done)
                    y_predicted = torch.squeeze(self.critic.forward(s1, a1))
            # compute critic loss, and update the critic
                    loss_critic = self.l_loss(y_predicted, y_expected.detach()).unsqueeze(0)
                    self.critic_optimizer.zero_grad()
                    loss_critic.backward()
                    self.critic_optimizer.step()
            
            #-----------optimize actor --------------------------------------
                    pred_a1 = self.actor.forward(s1)
                    pred_a1_copy = pred_a1.detach().numpy()
                    self.actor_logic.append(pred_a1_copy[-1][-1])
                    loss_actor = -self.critic.forward(s1, pred_a1).mean()
                    #entropy = torch.mean(pred_a1*torch.log(pred_a1))
                    loss_policy = loss_actor
                    self.loss_l1_list.append(loss_policy.item())
                    mse_policy = self.target_critic(s1,d1).mean()
                    loss_mse = self.mse(loss_actor, mse_policy)
                    self.loss_mse_list.append(loss_mse.item())
                    loss = sum([(1-self.lambda_mse)*loss_policy, self.lambda_mse*loss_mse])
                    self.loss_final_list.append(loss.item())
                    self.actor_optimizer.zero_grad()
                    loss.backward()
                    self.actor_optimizer.step()
            
                    soft_update(self.target_actor, self.actor, self.tau)
                    soft_update(self.target_critic, self.critic, self.tau)
        
        #self.actor.state_dict(self.target_actor.state_dict())
        #self.critic.state_dict(self.target_critic.state_dict())
        
    def get_exploitation_action(self, state):
        
        action = self.target_actor.forward(state).detach()
        return action.data.numpy()
    
    def get_exploration_action(self,state):
        
        action = self.actor.forward(state).detach()
        new_action = action.data.numpy()+self.noise.sample()
        new_action = np.clip(new_action,0,1)
        return new_action
    
    def save_models(self, episode_count, path_actor, path_critic):
        
        torch.save(self.target_actor.state_dict(),path_actor)
        torch.save(self.target_critic.state_dict(), path_critic)
    
    def load_models(self, episode):
        """
        checkpoint = torch.load(PATH)
        model.load_state_dict(checkpoint['modelA_state_dict'])
        """
        self.actor.load_state_dict(self.target_actor.state_dict())
        self.critic.load_state_dict(self.target_critic.state_dict())
        hard_update(self.target_actor, self.actor)
        hard_update(self.target_critic, self.critic)
    
#################  Main #################
        
start = datetime.datetime.now()
print("Simulation Started at:", start)

max_episodes = 1000
max_steps = 1000
max_buffer = 10000000
batch_size = 32
td_n = 10
energy_consumed_per_episode = []
episode_counter = []
step_counter = []
reward_sum_episode = []
mean_reward_steps = []
reward_stepwise = []
mean_energy_steps = []
mean_energy_episode = []
total_reward = 0
logic_m_1 = []
logic_a_1 = []
mse_1 = []
actor_1 = []
final_1 = []
q_val_network = []
td = []
silo = []
Hopper = []
loss_mse_1 = []
loss_actor_1 = []
loss_final = []
q_val  = []
td_loss = []
mass_exchanged = []
terminal_reached = []
actor_neurons = 20
critic_neurons = 20
ram_1 = MemoryBuffer(max_buffer)

env = bulk_good(max_steps, max_episodes)
for e in range(max_episodes):
    if e < 250:
        mse = 1
    elif 250 <= e <500:
        mse = 0.75
    elif 500 <= e <750:
        mse = 0.5
    elif 750<= e <1000:
        mse = 0.25
    elif 1000<= e <max_episodes:
        mse = 0
    
    trainer_1 = Trainer(2, 1, mse, ram_1, batch_size,actor_neurons,critic_neurons)    
    env.state_space_reset()
    x = env.initial_state()
    reached = x[33]
    total_energy_sim = 0
    total_reward = 0
    mass_transfer = 0
    states = []
    for s in range(max_steps):
        state_1 = [x[0]/20,x[3]/10]
        
        state_space_1 = torch.tensor(state_1).float()
        
        if e < 500:
            prob = (-0.089)*e+90
        else:
            prob = 1
        
        randomizer = randrange(0,3)
        
        if randomizer < prob:
            conveyor_motor_speed = trainer_1.get_exploration_action(state_space_1)*1800
        else:
            conveyor_motor_speed = trainer_1.get_exploitation_action(state_space_1)*1800
        #network_prediction.append(conveyor_motor_speed)
        Plc = plc()
        
        d_conv = Plc.get_Conveyor_Motor_Speed(x[0],x[3])
        #plc_prediction.append(d_conv)
        new_state = env.environment_bgs(s,e)
        new_silo_filllevel_1 = new_state[0]
        new_hopper_filllevel_1 = new_state[3]
        total_energy_sim += new_state[12]
        mean_energy_steps.append(new_state[12])
        reward_1 = new_state[21]
        mass_transfer += new_state[19]
        reached = new_state[20]
        total_reward += reward_1
        reward_stepwise.append(reward_1)
        silo.append(new_silo_filllevel_1)
        Hopper.append(new_hopper_filllevel_1)
        
        new_state_1 = [new_silo_filllevel_1/20, new_hopper_filllevel_1/10]
        new_state_space_1 = torch.tensor(new_state_1).float()
        
        ram_1.add(state_space_1.tolist(),(d_conv/1800),(conveyor_motor_speed/1800),reward_1/50,
                  new_state_space_1.tolist(), reached)
        trainer_1.optimize(s,max_steps,td_n)
        
        mse_1 = trainer_1.loss_mse_list
        actor_1 = trainer_1.loss_l1_list
        #print("A",actor_1)
        #time.sleep(2)
        final_1 = trainer_1.loss_final_list
        
        mse_logic = trainer_1.mse_logic
        actor_logic = trainer_1.actor_logic
        #print("steps:",s,"|episodes:",e)
        #time.sleep(1)
        if reached == 1:
            env.state_space_reset
            break
    mass_exchanged.append(mass_transfer)
    mean_reward_steps.append(np.mean(reward_stepwise))
    episode_counter.append(e)
    mean_energy_episode.append(np.mean(mean_energy_steps))
    energy_consumed_per_episode.append(total_energy_sim)
    reward_sum_episode.append(total_reward)
    
    logic_m_1.append(np.mean(mse_logic))
    logic_a_1.append(np.mean(actor_logic))
    q_val_network.append(np.mean(q_val))
    loss_mse_1.append(np.mean(mse_1))
    loss_actor_1.append(np.mean(actor_1))
    loss_final.append(np.mean(final_1))
    td_loss.append(np.mean(td))
    gc.collect()

    if e%300 == 0 and e!= 0:
        print('e:',e)
        #ram_1.clearmemory()
    if e == max_episodes-1 and e!= 0:
        print("bye")
        os.mkdir(time.strftime("%d_%a_%y"))
        os.chdir(time.strftime("%d_%a_%y"))
        torch.save(mass_exchanged,'mass_exchanged.pt')
        torch.save(energy_consumed_per_episode,'energy.pt')
        torch.save(terminal_reached,'terminal-reached.pt')
        torch.save(mean_energy_episode,'mean_energy_episode.pt')
        torch.save(episode_counter,'episode.pt')
        torch.save(silo,'silo-1.pt')
        torch.save(Hopper,'Hopper-1.pt')
        torch.save(step_counter,'steps.pt')
        torch.save(reward_sum_episode,'reward_sum_episodewise.pt')
        torch.save(mean_reward_steps,'mean_reward_stepwise.pt')
        torch.save(reward_stepwise,'reward_stepwise.pt')
        torch.save(logic_m_1,'logic_m.pt')
        torch.save(logic_a_1,'logic_a.pt')
        torch.save(loss_mse_1,'loss_mse.pt')
        torch.save(loss_actor_1,'loss_actor.pt')
        torch.save(loss_final,'loss_final.pt')


end = datetime.datetime.now()
print("Simulation ended at:",end)
print("duration:{}".format(end-start))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:26:23 2020

@author: at-lab
"""

from random import randrange,uniform
import scipy.integrate as integrate
from plc import plc
import time
################################### ENVIRONMENT ############################################





#################### Initial State for an episode ###################

class bulk_good:

    def __init__(self,max_steps,max_episodes):

        self.max_episodes = max_episodes
        self.max_steps = max_steps
        self.Silo_Filllevel_1 = uniform(0,20) # Initialization of Silo-1
        self.Silo_Filllevel_2 = uniform(0,20) # Initialization of Silo-2
        #print("i",self.Silo_Filllevel_2)
        self.Silo_Filllevel_3 = uniform(0,20) # Initialization of Silo-3

        self.Hopper_Filllevel_1 = uniform(0,10)  #Iniitialization of Hopper-1
        self.Hopper_Filllevel_2 = uniform(0,10)  #Initialization of Hopper-2
        self.Hopper_Filllevel_3 = uniform(0,10)  #Initialization of Hopper-3

        self.VP_Prev_2 = 0
        self.VP_Prev_3 = 0
        self.VP_Prev_4 = 0

        self.Rising_2 = 0
        self.Falling_2 = 0
        self.Rising_3 = 0
        self.Falling_3 = 0
        self.Rising_4 = 0
        self.Falling_4 = 0


        self.Q_Flip_2 = 0
        self.Q_Flip_3 = 0
        self.Q_Flip_4 = 0

        self.Q_Flip_Prev_2 = 0
        self.Q_Flip_Prev_3 = 0
        self.Q_Flip_Prev_4 = 0

        self.Saturator_2 = 0
        self.Saturator_3 = 0
        self.Saturator_4 = 0

        self.MF_S_H_1 = 0
        self.MF_S_H_2 = 0
        self.MF_S_H_3 = 0

        self.MF_VC_2 = 0
        self.MF_VC_3 = 0
        self.MF_VC_4 = 0

        self.Energy_Conveyor_Sim = 0
        self.Energy_VC_2_Sim = 0
        self.Energy_Vibration_Belt_Sim = 0
        self.Energy_VC_3_Sim = 0
        self.Energy_Rotary_Air_Lock_Sim = 0
        self.Energy_VC_4_Sim = 0
        self.Exchanged_Mass_Sim = 0
        self.reached = 0
        self.Total_Energy_Sim  = 0
        self.Total_Energy_Sim_Prev = 0
        self.mass_episodic = 0
        self.mass_steps_1 = 0
        ###########


        self.VP_2 = 1
        self.VP_3 = 1
        self.VP_4 = 1

        self.VP_Time_2 = 0
        self.VP_Time_3 = 0
        self.VP_Time_4 = 0


        self.reward = 0
        self.Total_Reward = 0
        self.dem = 0
        self.Mass_episodic = 0
        self.count = 0
        self.Mass = []
        self.energy = []


    def initial_state(self):

        self.Silo_Filllevel_1 = uniform(0,20) # Initialization of Silo-1
        self.Silo_Filllevel_2 = uniform(0,20)# Initialization of Silo-2
        self.Silo_Filllevel_3 = uniform(0,20)# Initialization of Silo-3

        self.Hopper_Filllevel_1 = uniform(0,10)   #Iniitialization of Hopper-1
        self.Hopper_Filllevel_2 = uniform(0,10)  #Initialization of Hopper-2
        self.Hopper_Filllevel_3 = uniform(0,10)  #Initialization of Hopper-3

        self.VP_Prev_2 = randrange(0,2)
        self.VP_Prev_3 = randrange(0,2)
        self.VP_Prev_4 = randrange(0,2)

        self.Rising_2 = randrange(0,2)
        self.Falling_2 = randrange(0,2)
        self.Rising_3 = randrange(0,2)
        self.Falling_3 = randrange(0,2)
        self.Rising_4 = randrange(0,2)
        self.Falling_4 = randrange(0,2)

        self.Q_Flip_2 = randrange(0,2)
        self.Q_Flip_3 = randrange(0,2)
        self.Q_Flip_4 = randrange(0,2)

        self.Q_Flip_Prev_2 = randrange(0,2)
        self.Q_Flip_Prev_3 = randrange(0,2)
        self.Q_Flio_Prev_4 = randrange(0,2)

        self.Saturator_2 = randrange(0,2)
        self.Saturator_3 = randrange(0,2)
        self.Saturator_4 = randrange(0,2)
        self.Silo_Empty_1 = 0
        self.Silo_Empty_2 = 0
        self.Silo_Empty_3 = 0
        self.Hopper_Empty_1 = 0
        self.Hopper_Empty_2 = 0
        self.Hopper_Empty_3 = 0
        self.Total_Energy_Sim = 0
        self.reward = 0

        return self.Silo_Filllevel_1,self.Silo_Filllevel_2,self.Silo_Filllevel_3,self.Hopper_Filllevel_1,self.Hopper_Filllevel_2,self.Hopper_Filllevel_3,self.VP_Prev_2,self.VP_Prev_3,self.VP_Prev_4,self.Rising_2,self.Falling_2,self.Rising_3,self.Falling_3,self.Rising_4,self.Falling_4,self.Q_Flip_2,self.Q_Flip_3,self.Q_Flip_4,self.Q_Flip_Prev_2,self.Q_Flip_Prev_3,self.Q_Flio_Prev_4,self.Saturator_2,self.Saturator_3,self.Saturator_4,self.Silo_Empty_1,self.Silo_Empty_2,self.Silo_Empty_3,self.Hopper_Empty_1,self.Hopper_Empty_2,self.Hopper_Empty_3,self.MF_VC_2,self.MF_VC_3,self.MF_VC_4,self.reached


############### State Space Reset ################


######################################### BULK GOOD SYSTEM #####################################

    def environment_bgs(self,steps_in_episode,ep):
        self.steps = steps_in_episode
        self.episodes = ep
        Plc = plc()
        #print("I am IN")

        bigloop = 0
        t = 0
        count = 0
        while bigloop <=100:  # 10 secs
            count += 1
            #print("count:",count)
            ##################### Station 1 #####################

            #### Substation 1 - Conveyor Belt - RPM to Mass flow ####
            # Massflow Silo to Hopper

            #### SILO_STATE ######
            #print("Silo:",self.Silo_Filllevel_1)
            ######################
            self.Conveyor_Motor_Speed = plc.get_Conveyor_Motor_Speed(Plc,self.Silo_Filllevel_1,self.Hopper_Filllevel_1)
            #self.Conveyor_Motor_Speed = 1800
            #print("Conveyor",self.Conveyor_Motor_Speed)
            self.MF_S_H_1 = self.Conveyor_Motor_Speed * 0.01 / 60 * self.Silo_Empty_1   # Max-Value = 0.3 and Min-value = 0
            # if self.MF_S_H_1 == 0:
            #     print("No flow Silo to Hopper-1")

            self.cms = self.Conveyor_Motor_Speed

            # Energy - Conveyor Belt
            #print("Powerconsumption",self.Conveyor_Motor_Speed*(-81.0493 + 0.5558316*self.cms - 0.0008993839*self.cms**2 + 6.578498e-7*self.cms**3 - 2.197611e-10*self.cms**4 + 2.721772e-14*self.cms**5)/(6*1000))

            f_cms = lambda x: self.Conveyor_Motor_Speed*(-81.0493 + 0.5558316*self.cms - 0.0008993839*self.cms**2 + 6.578498e-7*self.cms**3 - 2.197611e-10*self.cms**4 + 2.721772e-14*self.cms**5)/(6*1000)
            energy,err = integrate.quad(f_cms,t,t+0.1)
            #print("energy",energy)

            self.Energy_Conveyor_Sim = self.Energy_Conveyor_Sim +  energy
            #print("Energy_conveyor",self.Energy_Conveyor_Sim)

            #### Substation 2 - Silo-1 ####

            # Silo Fill level

            #print("Mass_Flow_to_Hopper",self.MF_S_H_1 * (-1))

            f_sfl_1 = lambda x: ((self.MF_VC_4/2)-self.MF_S_H_1)
            fill,err = integrate.quad(f_sfl_1,t,t+0.1)

            #print("fill",fill)

            self.Silo_Filllevel_1 = self.Silo_Filllevel_1 + fill
            #Mass_Silo_1 = Mass_Silo_1 + fill
            if self.Silo_Filllevel_1 > 20:
                self.Silo_Filllevel_1 = 20
            elif self.Silo_Filllevel_1 < 0:
                self.Silo_Filllevel_1 = 0

            #print("Silo_1:",self.Silo_Filllevel_1)
            # Silo Empty

            if self.Silo_Filllevel_1 >= 0.1:
                self.Silo_Empty_1 = 1
            else:
                self.Silo_Empty_1 = 0

            #### Substation 3 - Hopper-1 ####

            # Hopper Fill level
            #print("Hopper_1:",self.Hopper_Filllevel_1)

            f_hfl_1 = lambda x: (self.MF_S_H_1 - self.MF_VC_2)

            fill, err = integrate.quad(f_hfl_1, t, t+0.1)
            #print("fill",fill)
            self.Hopper_Filllevel_1 = self.Hopper_Filllevel_1 + fill
            #print("Hopper_1:",self.Hopper_Filllevel_1)
            if self.Hopper_Filllevel_1>10:
                self.Hopper_Filllevel_1 = 10
            elif self.Hopper_Filllevel_1<0:
                self.Hopper_Filllevel_1 = 0


            # Hopper Empty

            if self.Hopper_Filllevel_1 >= 0.1:
                self.Hopper_Empty_1 = 1
            else:
                self.Hopper_Empty_1 = 0
            #print("Hopper_Fill_1",self.Hopper_Filllevel_1,"Hopper_empty_1",self.Hopper_Empty_1)

            ##################### Station 2 #####################

            #### Substation 1 - Vacuum Pump-2 ####

            # Massflow - Previous Hopper to Silo
            self.VP_Time_2 = plc.get_vp_2(Plc,self.Hopper_Filllevel_1,self.Silo_Filllevel_2)
            #self.VP_Time_2 = 10
            if t >= self.VP_Time_2:           # VP_Time_2 is initialized always to 10
                self.VP_2 = 0
            else:
                self.VP_2 = 1
                                             # VP_Prev_2 is initialized between 0 to 1
            #print("VP_Prev_2",self.VP_Prev_2)

            if self.VP_2 - self.VP_Prev_2 > 0:              # To know if the quantity of material is rising or falling in the VP
                self.Rising_2 = 1
                self.Falling_2 = 0
            elif self.VP_2 - self.VP_Prev_2 <0:
                self.Rising_2 = 0
                self.Falling_2 = 1     #
            else:                                  #
                self.Rising_2 = 0
                self.Falling_2 = 0     #

            self.VP_Prev_2 = self.VP_2       #Making our Vaccum Pump to stop

            #print("rising",self.Rising_2,"falling",self.Falling_2)

            if self.Rising_2 == 0 and self.Falling_2 == 0:    # SR Flip-Flop equivalent
                self.Q_Flip_2 = self.Q_Flip_Prev_2
            elif self.Rising_2 == 0 and self.Falling_2 == 1:
                self.Q_Flip_2 = 1
            elif self.Rising_2 == 1 and self.Falling_2 == 0:
                self.Q_Flip_2 = 0
            elif self.Rising_2 == 1 and self.Falling_2 == 1:
                self.Q_Flip_2 = 0

            self.Q_Flip_Prev_2 = self.Q_Flip_2
            #print("t",t)

            if self.Q_Flip_2 == 1:
                self.MF_VC_2 = 0
            elif self.Q_Flip_2 == 0:
                self.Saturator_2 = t - 0.567
            #print(self.Saturator_2)


            if self.Saturator_2 >= 4:
                self.Saturator_2 = 4
            elif self.Saturator_2 <= 0:
                self.Saturator_2 = 0


            self.MF_VC_2 = ((0.0664 * self.Saturator_2) + 0.464) * (self.Hopper_Empty_1)
            #print("Saturator_2",self.Saturator_2,"MF_VC_2",self.MF_VC_2)

            # Energy - Vacuum Pump

            f_vp_2 = lambda x: (self.VP_2 * 0.305)

            energy,err = integrate.quad(f_vp_2, t, t+0.1)

            self.Energy_VC_2_Sim = self.Energy_VC_2_Sim + energy

            #### Substation 2- Vibration Belt ####

            # Massflow Silo to Hopper

            if self.Silo_Filllevel_2 >= 0.1:
                self.Silo_Empty_2 = 1
            else:
                self.Silo_Empty_2 = 0

            self.Vibration_Belt_Start = plc.get_Vibration_Belt_Start(Plc,self.Silo_Filllevel_2,self.Hopper_Filllevel_2)
            #self.Vibration_Belt_Start = 1

            self.MF_S_H_2 = self.Vibration_Belt_Start * 0.4 * self.Silo_Empty_2


            f_env = lambda x: (26.9 * self.Vibration_Belt_Start / 1000)
            energy, err = integrate.quad(f_env,t,t+0.1)

            self.Energy_Vibration_Belt_Sim = self.Energy_Vibration_Belt_Sim + energy

            #### Substation 3 - Silo ####

            # Silo Fill level

            #print("Material_flown_Overall",fill)

            f_sfl_2 = lambda x: (self.MF_VC_2 - self.MF_S_H_2)
            fill,err = integrate.quad(f_sfl_2,t,t+0.1)
            #print("Material_flown_Overall",fill)
            #print(self.Silo_Filllevel_2)
            #time.sleep(2)

            self.Silo_Filllevel_2  = self.Silo_Filllevel_2 + fill
            #Mass_Silo_2 = Mass_Silo_2 + fill
            if self.Silo_Filllevel_2 > 20:
                self.Silo_Filllevel_2 = 20
            elif self.Silo_Filllevel_2 < 0:
                self.Silo_Filllevel_2 = 0


            #### Substation 3 - Hopper ####

            # Hopper Fill level

            f_hfl_2 = lambda x: (self.MF_S_H_2 - self.MF_VC_3)

            fill,err = integrate.quad(f_hfl_2,t,t+0.1)

            self.Hopper_Filllevel_2 = self.Hopper_Filllevel_2 + fill

            if self.Hopper_Filllevel_2 > 10:
                self.Hopper_Filllevel_2 = 10
            elif self.Hopper_Filllevel_2 < 0:
                self.Hopper_Filllevel_2 = 0

            # Hopper Empty

            if self.Hopper_Filllevel_2 >= 0.1:
                self.Hopper_Empty_2 = 1
            else:
                self.Hopper_Empty_2 = 0
            #print("Hopper_2",self.Hopper_Filllevel_2)


            ##################### Station 3 #####################

            #### Substation 1 - Vacuum Pump ####
            self.VP_Time_3 = plc.get_vp_3(Plc,self.Hopper_Filllevel_2,self.Silo_Filllevel_3)
            #self.VP_Time_3 = 10
            if t >= self.VP_Time_3:
                self.VP_3 = 0
            else:
                self.VP_3 = 1

            #print("diff",self.VP_3-self.VP_Prev_3)
            if self.VP_3 - self.VP_Prev_3 > 0:              # To know if the quantity of material is rising or falling in the VP
                self.Rising_3 = 1
                self.Falling_3 = 0      #
            elif self.VP_3 - self.VP_Prev_3 <0:             #
                self.Rising_3 = 0
                self.Falling_3 = 1      #
            elif self.VP_3 - self.VP_Prev_3 == 0:            #
                self.Rising_3 = 0
                self.Falling_3 = 0      #

            self.VP_Prev_3 = self.VP_3
            #print("Rising_3",self.Rising_3,"Falling",self.Falling_3)

            if self.Rising_3 == 0 and self.Falling_3 == 0:    # SR Flip-Flop equivalent
                self.Q_Flip_3 = self.Q_Flip_Prev_3
            elif self.Rising_3 == 0 and self.Falling_3 == 1:
                self.Q_Flip_3 = 1
            elif self.Rising_3 == 1 and self.Falling_3 == 0:
                self.Q_Flip_3 = 0
            elif self.Rising_3 == 1 and self.Falling_3 == 1:
                self.Q_Flip_3 = 0

            self.Q_Flip_Prev_3 = self.Q_Flip_3

            if self.Q_Flip_3 == 1:
                self.MF_VC_3 = 0
            elif self.Q_Flip_3 == 0:
                self.Saturator_3 = t - 0.979
            #print("Saturator_3:",self.Saturator_3)

            if self.Saturator_3 >= 8.5:
                self.Saturator_3 = 8.5
            elif self.Saturator_3 <= 0:
                self.Saturator_3 = 0


            #print("Hopper_Fill_2",self.Hopper_Filllevel_2,"Saturator_3",self.Saturator_3)


            self.MF_VC_3 = ((0.0192 * self.Saturator_3)+0.3535) * (self.Hopper_Empty_2)
            #print("Hopper_empty_2",self.Hopper_Empty_2,"Saturator_3",self.Saturator_3,"MF_VC_3",self.MF_VC_3)

            # Energy - Vacuum Pump

            f_vp_3 = lambda x: (self.VP_3 * 0.456)

            energy,err = integrate.quad(f_vp_3,t,t+0.1)
            #print("energy",energy)

            self.Energy_VC_3_Sim = self.Energy_VC_3_Sim + energy

            #### Substation 2 - Rotary Air lock ####

            # Massflow Silo to Hopper

            if self.Silo_Filllevel_3 >= 0.1:
                self.Silo_Empty_3 = 1
            else:
                self.Silo_Empty_3 = 0

            self.Dosing_Speed = plc.get_Dosing_Speed(Plc,self.Silo_Filllevel_3,self.Hopper_Filllevel_3)
            #self.Dosing_Speed = 1500
            #print("Silo",self.Silo_Filllevel_3,"Hopper",self.Hopper_Filllevel_3)
            #print("Dosing_Speed",self.Dosing_Speed)
            self.MF_S_H_3 = (self.Dosing_Speed) * (self.Silo_Empty_3) * 0.01249 / 60
            #print("Dosing_Speed:",self.Dosing_Speed,"|MF_S_H_3:",self.MF_S_H_3,"|Silo_Empty_3:",self.Silo_Empty_3)

            #print("MF_S_H_3",self.MF_S_H_3)

            # Energy Rotary Air Lock

            f_eral = lambda x: (self.Dosing_Speed * 370 / (1500 * 1000))

            energy,err = integrate.quad(f_eral,t,t+0.1)

            self.Energy_Rotary_Air_Lock_Sim = self.Energy_Rotary_Air_Lock_Sim + energy

            #### Substation 3 - Silo ####

            # Silo Fill level

            f_sfl_3 = lambda x: (self.MF_VC_3 - self.MF_S_H_3)
            fill,err = integrate.quad(f_sfl_3,t,t+0.1)

            self.Silo_Filllevel_3  = self.Silo_Filllevel_3 + fill
            #Mass_Silo_3 = Mass_Silo_3 + fill
            if self.Silo_Filllevel_3 > 20:
                self.Silo_Filllevel_3 = 20
            elif self.Silo_Filllevel_3 < 0:
                self.Silo_Filllevel_3 = 0

            #### Substation 3 - Hopper ####

            # Hopper Fill level
            #print("MF_S_H_3:",self.MF_S_H_3,"MF_VC_4:",self.MF_VC_4)
            f_hfl_3 = lambda x: (self.MF_S_H_3-(self.MF_VC_4/2)) # CHANGED HERE EQUATION
            fill,err = integrate.quad(f_hfl_3,t,t+0.1)
            #print("fill",fill)

            self.Hopper_Filllevel_3 = self.Hopper_Filllevel_3 + fill
            #print("Hopper_3:",self.Hopper_Filllevel_3)
            if self.Hopper_Filllevel_3 > 20:
                self.Hopper_Filllevel_3 = 20
            elif self.Hopper_Filllevel_3 < 0:
                self.Hopper_Filllevel_3 = 0


            # Hopper Empty

            if self.Hopper_Filllevel_3 >= 0.1:
                self.Hopper_Empty_3 = 1
            else:
                self.Hopper_Empty_3 = 0

            ###### Station-4 ##########
            self.VP_Time_4 = plc.get_vp_4(Plc,self.Hopper_Filllevel_3,self.Silo_Filllevel_1)
            #self.VP_Time_4
            #print("VP_time",self.VP_Time_4)
            if t >= self.VP_Time_4:
                self.VP_4 = 0
            else:
                self.VP_4 = 1


            if self.VP_4 - self.VP_Prev_4 > 0:              # To know if the quantity of material is rising or falling in the VP
                self.Rising_4 = 1
                self.Falling_4 = 0      #
            elif self.VP_4 - self.VP_Prev_4 <0:             #
                self.Rising_4 = 0
                self.Falling_4 = 1      #
            elif self.VP_4 - self.VP_Prev_4 == 0:            #
                self.Rising_4 = 0
                self.Falling_4 = 0      #

            self.VP_Prev_4 = self.VP_4
            #print("Rising_3",self.Rising_3,"Falling",self.Falling_3)

            if self.Rising_4 == 0 and self.Falling_4 == 0:    # SR Flip-Flop equivalent
                self.Q_Flip_4 = self.Q_Flip_Prev_4
            elif self.Rising_4 == 0 and self.Falling_4 == 1:
                self.Q_Flip_4 = 1
            elif self.Rising_4 == 1 and self.Falling_4 == 0:
                self.Q_Flip_4 = 0
            elif self.Rising_4 == 1 and self.Falling_4 == 1:
                self.Q_Flip_4 = 0

            self.Q_Flip_Prev_4 = self.Q_Flip_4

            if self.Q_Flip_4 == 1:
                self.MF_VC_4 = 0
            elif self.Q_Flip_4 == 0:
                self.Saturator_4 = t - 0.567

            if self.Saturator_4 >= 4:
                self.Saturator_4 = 4
            elif self.Saturator_4 <= 0:
                self.Saturator_4 = 0

            self.MF_VC_4 = ((0.0664 * self.Saturator_4)+0.464) * (self.Silo_Empty_1)
            #print("flow",self.MF_VC_4,"Saturator_4:",self.Saturator_4)

            # Energy - Vacuum Pump

            f_vp_4 = lambda x: (self.VP_4 * 0.305)

            energy,err = integrate.quad(f_vp_4,t,t+0.1)
            #print("energy",energy)

            self.Energy_VC_4_Sim = self.Energy_VC_4_Sim + energy

            f_demand = lambda x: self.MF_S_H_3                 # Overall Mass transported by the system
            self.dem,err = integrate.quad(f_demand,t,t+0.1)

            self.Exchanged_Mass_Sim = self.Exchanged_Mass_Sim + self.dem
            #print("MASS",self.Exchanged_Mass_Sim,"step:",self.steps)
            #time.sleep(1)

            ##########################################################

            t = t + 0.1                             # Next time step
            #print("t",t     )
            bigloop = bigloop + 1
            #print("MASS",self.Exchanged_Mass_Sim,)
            #print("bigloop",bigloop)
            ################################################################################################################
        #self.Energy_Previous = self.Total_Energy_Sim
        self.Total_Energy_Sim = sum([self.Energy_Conveyor_Sim, self.Energy_VC_2_Sim, self.Energy_Vibration_Belt_Sim, self.Energy_VC_3_Sim, self.Energy_Rotary_Air_Lock_Sim, self.Energy_VC_4_Sim])
        self.Mass.append(self.Exchanged_Mass_Sim)
        #print(max(self.Mass))
        self.energy.append(self.Total_Energy_Sim)
        ############ Rewards ###########
        #### Terminal State ####
        #print("mass:",self.Exchanged_Mass_Sim - max(self.Mass))
        #print("energy:",self.Total_Energy_Sim - min(self.energy))
        self.reward = 0
        if self.Exchanged_Mass_Sim-self.mass_steps_1 >=0:
                self.reward += 1
        else:
                self.reward += 0
        self.mass_steps_1 = self.Exchanged_Mass_Sim

        if self.Total_Energy_Sim-self.Total_Energy_Sim_Prev<=0:
            self.reward += 1
        else:
            self.reward += 0

        if self.steps == self.max_steps-1:
            self.reward = -1
        if self.steps%10==0:
            self.mass_episodic += self.Exchanged_Mass_Sim
            #print(self.mass_episodic)

        if self.mass_episodic >= 100000:
            self.reward += 50
            self.reached = 1
            self.mass_episodic = 0
        else:
            self.reached = 0

        #print(self.reward)
        return self.Silo_Filllevel_1,self.Silo_Filllevel_2,self.Silo_Filllevel_3,self.Hopper_Filllevel_1,self.Hopper_Filllevel_2,self.Hopper_Filllevel_3,self.Energy_Conveyor_Sim,self.Energy_VC_2_Sim,self.Energy_Vibration_Belt_Sim,self.Energy_VC_3_Sim,self.Energy_Rotary_Air_Lock_Sim,self.Energy_VC_4_Sim,self.Total_Energy_Sim,self.MF_VC_2,self.MF_VC_3,self.MF_VC_4,self.MF_S_H_1,self.MF_S_H_2,self.MF_S_H_3,self.Exchanged_Mass_Sim,self.reached,self.reward
        #return self.Silo_Filllevel_1,self.Hopper_Filllevel_1, self.MF_S_H_1, self.Conveyor_Motor_Speed, self.MF_VC_2, self.Saturator_2 , self.Silo_Filllevel_2,self.Hopper_Filllevel_2,self.MF_S_H_2,self.Vibration_Belt_Start,self.MF_VC_3,self.Saturator_3,self.Silo_Filllevel_3,self.Hopper_Filllevel_3,self.MF_S_H_3,self.Dosing_Speed,self.MF_VC_4,self.Saturator_4,self.Silo_Empty_1

#     0 Silo_Filllevel_1      # 7 Energy_VC_2_Sim              #14 VP_Time_2    #21 Silo_Empty_1      #28 Saturator_3          #35 reward_3          #42 Total_Reward_4
#    1 Silo_Filllevel_2      # 8 Energy_Vibration_Belt_Sim    #15 VP_Time_3    #22 Hopper_Empty_1    #29 VP_Prev_2            #36 reward_4          #43 Total_Reward_5
#    2 Silo_Filllevel_3      # 9 Energy_VC_3_Sim              #16 MF_VC_2      #23 Q_Flip_2          #30 VP_Prev_3            #37 reward_5          #44 Total_Reward_6
#    3 Hopper_Filllevel_1    #10 Energy_Rotary_Air_Lock_Sim   #17 MF_VC_3      #24 Q_Flip_3          #31 Exchanged_Mass_Sim   #38 reward_6          #45 Demand
#    4 Hopper_Filllevel_2    #11 Total_Energy_Sim             #18 MF_S_H_1     #25 Q_Flip_Prev_2     #32 reached              #39 Total_Reward_1
#    5 Hopper_Filllevel_3    #12 VP_2                         #19 MF_S_H_2     #26 Q_Flip_Prev_3     #33 reward_1             #40 Total_Reward_2
#    6 Energy_Conveyor_Sim   #13 VP_3                         #20 MF_S_H_3     #27 Saturator_2       #34 reward_2             #41 Total_Reward_3
    ##################################################################################################################
    ##################################################################################################################

    def state_space_reset(self):

        self.Exchanged_Mass_Sim = 0
        self.Total_Energy_Sim_Prev = 0
        self.Exchanged_Mass_Sim_Prev = 0
        self.Energy_Conveyor_Sim = 0
        self.Energy_VC_2_Sim = 0
        self.Energy_Vibration_Belt_Sim = 0
        self.Energy_VC_3_Sim = 0
        self.Energy_Rotary_Air_Lock_Sim = 0
        self.Energy_VC_4_Sim = 0
        self.Total_Energy_Sim = 0
        self.reached = 0
        self.Total_Reward = 0
        self.reward = 0
        self.Energy_Episode = 0
        self.Silo_Filllevel_1 = 0
        self.Silo_Filllevel_2 = 0
        self.Silo_Filllevel_3 = 0
        self.Hopper_Filllevel_1 = 0
        self.Hopper_Filllevel_2 = 0
        self.Hopper_Filllevel_3 = 0


        return self.Exchanged_Mass_Sim,self.Total_Energy_Sim_Prev,self.Exchanged_Mass_Sim_Prev,self.Energy_Conveyor_Sim,self.Energy_VC_2_Sim,self.Energy_Vibration_Belt_Sim,self.Energy_VC_3_Sim,self.Energy_Rotary_Air_Lock_Sim,self.Energy_VC_4_Sim,self.Total_Energy_Sim,self.reached,self.Total_Reward,self.reward,self.Energy_Episode,self.Silo_Filllevel_1,self.Silo_Filllevel_2,self.Silo_Filllevel_3,self.Hopper_Filllevel_1,self.Hopper_Filllevel_2,self.Hopper_Filllevel_3


#for i in range(20):
###
#blk = bulk_good(1000,200)

# # ####
#a = []
#a = blk.initial_state()
# b = []
# c = []
# d = []
# e = []
# f = []
# g = []
# h = []
# I = []
# j = []
# k = []
# l = []
# m = []
# n = []
# o = []
# p = []
# q = []
# r = []
# t = []
#for i in range(1000):
#     #blk = bulk_good()
#     s = blk.environment_bgs(1000,200)
#     a.append(s[0])
#     b.append(s[1])
#     c.append(s[2])
#     d.append(s[3])
#     e.append(s[4])
#     f.append(s[5])
#     g.append(s[6])
#     h.append(s[7])
#     I.append(s[8])
#     j.append(s[9])
#     k.append(s[10])
#     l.append(s[11])
#     m.append(s[12])
#     n.append(s[13])
#     o.append(s[14])
#     p.append(s[15])
#     q.append(s[16])
#     r.append(s[17]/4.575)
#     #t.append(s[18])
#      #print(a)


# import matplotlib.pyplot as plt

# #plt.figure(10.0,10.0)
# plt.subplot(18,1,1),plt.plot(a,label='Silo_1'),plt.legend()
# plt.subplot(18,1,2),plt.plot(b,label='Hopper_1'),plt.legend()
# plt.subplot(18,1,3),plt.plot(c,label='MF_S_H_1'),plt.legend()
# plt.subplot(18,1,4),plt.plot(d,label='Conveyor'),plt.legend()
# plt.subplot(18,1,5),plt.plot(e,label='MF_VC_2'),plt.legend()
# plt.subplot(18,1,6),plt.plot(f,label='Saturator_2'),plt.legend()
# plt.subplot(18,1,7),plt.plot(g,label='Silo_2'),plt.legend()
# plt.subplot(18,1,8),plt.plot(h,label='Hopper_2'),plt.legend()
# plt.subplot(18,1,9),plt.plot(I,label='MF_S_H_2'),plt.legend()
# plt.subplot(18,1,10),plt.plot(j,label='Vibration'),plt.legend()
# plt.subplot(18,1,11),plt.plot(k,label='MF_VC_3'),plt.legend()
# plt.subplot(18,1,12),plt.plot(l,label='Saturator_3'),plt.legend()
# plt.subplot(18,1,13),plt.plot(m,label='Silo_3'),plt.legend()
# plt.subplot(18,1,14),plt.plot(n,label='Hopper_3'),plt.legend()
# plt.subplot(18,1,15),plt.plot(o,label='MF_S_H_3'),plt.legend()
# plt.subplot(18,1,16),plt.plot(p,label='Dosing_Speed'),plt.legend()
# plt.subplot(18,1,17),plt.plot(q,label='MF_VC_4'),plt.legend()
# plt.subplot(18,1,18),plt.plot(r,label='Saturator_4'),plt.legend()
#plt.subplot(5,1,5),plt.plot(t,label='Silo-empty_1'),plt.legend()

#plt.plot(a,'b',label='Silo_1'),plt.legend()
#plt.plot(n,'r',label='Hopper_3'),plt.legend()
# plt.plot(q,'g',label='MF_VC_4'),plt.legend()
# plt.plot(r,'r',label='Saturator_4'),plt.legend()
# plt.plot(t,'b',label='Silo_empty_1'),plt.legend()

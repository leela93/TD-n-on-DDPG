#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 13:46:13 2020

@author: at-lab
"""
class plc:
    
    def __init__(self):
        pass
    
            
    
        
    def get_Conveyor_Motor_Speed(self,Silo_Filllevel_1,Hopper_Filllevel_1):
        d_cms = 0
        self.Silo_Filllevel_1 = Silo_Filllevel_1
        self.Hopper_Filllevel_1 = Hopper_Filllevel_1
        ##### SILO-1 ########
#        print("Silo_Filllevel_1",self.Silo_Filllevel_1)
#        print("Hopper_Filllevel_1",self.Hopper_Filllevel_1)
        if self.Silo_Filllevel_1 >= 17.45:
            self.silo_full_1 = 1                # Here `1´ is signal for full
        else:
            self.silo_full_1 = 0

        if self.Silo_Filllevel_1 < 1:
            self.silo_empty_1 = 1               # Here `1´ is signal for empty 
        else:
            self.silo_empty_1 = 0

        ###### HOPPER-2 #######
        if self.Hopper_Filllevel_1 >= 9.5 :
            self.hopper_full_1 = 1              # Here `1´ is signal for full  
        else:
            self.hopper_full_1 = 0

        if self.Hopper_Filllevel_1 < 1:
            self.hopper_empty_1 = 1              # Here `1´ is signal for empty 
        else:
            self.hopper_empty_1 = 0
        #### CONTROL POLICIES-CONVEYOR ####
        #if (self.hopper_full_1  == 1 and self.silo_empty_1 == 1) or (self.silo_empty_1==1 and self.hopper_empty_1==1) or (self.silo_full_1==1 and self.hopper_full_1==1):    # Previous buffe (Silo) is empty or next buffe (Hopper) is full
        if self.silo_empty_1 == 1 or self.hopper_full_1 ==1:        
            d_cms = 0
        else:
             d_cms = 1800
    
        return d_cms
    
    def get_vp_2(self,Hopper_Filllevel_1,Silo_Filllevel_2,):
        Saturator_2 = 0
        self.Hopper_Filllevel_1 = Hopper_Filllevel_1
        self.Silo_Filllevel_2 = Silo_Filllevel_2
         ###### HOPPER-1 #######
        #print("Silo_Filllevel_2",self.Silo_Filllevel_2)
        #print("Hopper_Filllevel_1",self.Hopper_Filllevel_1)
        #print("Silo_Filllevel_2",self.Silo_Filllevel_2)
        if self.Hopper_Filllevel_1>=9.45:
            self.hopper_full_1 = 1              # Here `1´ is signal for full
        else:
            self.hopper_full_1 = 0

        if self.Hopper_Filllevel_1 < 1:
            self.hopper_empty_1 = 1              # Here `1´ is signal for empty 
        else:
            self.hopper_empty_1 = 0
            
        ####### SILO-2 #######
        if self.Silo_Filllevel_2 >= 17.45:
            self.silo_full_2 = 1                      # Here `1´ is signal for full
        else:
            self.silo_full_2 = 0
        
        if self.Silo_Filllevel_2 < 1:
            self.silo_empty_2 = 1                      # Here `1´ is signal for empty 
        else:
            self.silo_empty_2 = 0
        
        
        #### CONTROL_POLICIES @ VP2 #####
        
        if self.hopper_empty_1 == 1 or self.silo_full_2 == 1:    # Previous buffer is empty and next buffer is full
                Saturator_2 = 0
        else:
            Saturator_2 = 10
        return Saturator_2
    
    def get_Vibration_Belt_Start(self,Silo_Filllevel_2,Hopper_Filllevel_2):
        #print("Silo_Filllevel_2",Silo_Filllevel_2)
        #print("Hopper_Filllevel_2",Hopper_Filllevel_2)
        Vibration_Belt_Start = 0
        self.Silo_Filllevel_2 = Silo_Filllevel_2
        self.Hopper_Filllevel_2 = Hopper_Filllevel_2
        ####### SILO-2 ##########
        ##print("Hopper_Filllevel_2",self.Hopper_Filllevel_2)
        if self.Silo_Filllevel_2>=17.45:
            self.silo_full_2 = 1                      # Here `1´ is signal for full
        else:
            self.silo_full_2 = 0
        
        if self.Silo_Filllevel_2 < 1:
            self.silo_empty_2 = 1                      # Here `1´ is signal for empty 
        else:
            self.silo_empty_2 = 0
        
        ###### HOPPER-2 #####
        
        #print("Hopper_Filllevel_2=",Hopper_Filllevel_2)
        
        if self.Hopper_Filllevel_2 >=9.45:
            self.hopper_full_2 = 1                    # Here `1´ is signal for full
        else:
            self.hopper_full_2 = 0
            
        
        if self.Hopper_Filllevel_2 < 1:
            self.hopper_empty_2 = 1                    # Here `1´ is signal for empty 
        else:
            self.hopper_empty_2 = 0
        ###### CONTROL_POLICIES @ VIBRATION-BELT ######
        if self.silo_empty_2 == 1 or self.hopper_full_2 == 1:  # Previous buffe is empty or next buffer is full
            Vibration_Belt_Start  = 0
        else:
            Vibration_Belt_Start = 1
            
        return Vibration_Belt_Start
    
    def get_vp_3(self,Hopper_Filllevel_2,Silo_Filllevel_3):
        Saturator_3 = 0
        self.Hopper_Filllevel_2 = Hopper_Filllevel_2
        self.Silo_Filllevel_3 = Silo_Filllevel_3
         ###### HOPPER-1 #######
        #print("Silo_Filllevel_2",self.Silo_Filllevel_2)
        #print("Hopper_Filllevel_1",self.Hopper_Filllevel_1)
        #print("Silo_Filllevel_2",self.Silo_Filllevel_2)
        if self.Hopper_Filllevel_2 >=9.45:
            self.hopper_full_2 = 1              # Here `1´ is signal for full
        else:
            self.hopper_full_2 = 0

        if self.Hopper_Filllevel_2 < 1:
            self.hopper_empty_2 = 1              # Here `1´ is signal for empty 
        else:
            self.hopper_empty_2 = 0
            
        ####### SILO-2 #######
        if self.Silo_Filllevel_3 >= 17.45:
            self.silo_full_3 = 1                      # Here `1´ is signal for full
        else:
            self.silo_full_3 = 0
        
        if self.Silo_Filllevel_3 < 1:
            self.silo_empty_3 = 1                      # Here `1´ is signal for empty 
        else:
            self.silo_empty_3 = 0
        
        
        #### CONTROL_POLICIES @ VP3 #####
        
        if self.hopper_empty_2 == 1 or self.silo_full_3 == 1:  # Previous buffer is empty or next buffer is full
                Saturator_3 = 0
        else:
            Saturator_3 = 10
        return Saturator_3
    
    def get_Dosing_Speed(self,Silo_Filllevel_3,Hopper_Filllevel_3):
        Dosing_Speed = 0
        self.Silo_Filllevel_3 = Silo_Filllevel_3
        self.Hopper_Filllevel_3 = Hopper_Filllevel_3
        ###### SILO-3 #######
        #print("Hopper_Filllevel_1",self.Hopper_Filllevel_1)
        if  self.Silo_Filllevel_3 >= 17.45:
            self.silo_full_3 = 1                      # Here `1´ is signal for full
        else:
            self.silo_full_3 = 0
            
        #print("silo_full_3=",silo_full_3)
        
        if self.Silo_Filllevel_3 < 1:
            self.silo_empty_3 = 1                     # Here `1´ is signal for empty
        else:
            self.silo_empty_3 = 0
        
        ####### HOPPER-3 #######
        
        if self.Hopper_Filllevel_3 >=9.45:
            self.hopper_full_3 = 1 
        else:
            self.hopper_full_3 = 0

        if self.Hopper_Filllevel_3 < 1:
            self.hopper_empty_3 = 1
        else:
            self.hopper_empty_3 = 0
        
        ##### CONTORL FOR DOSING SPEED #####
        if self.silo_empty_3 == 1 or self.hopper_full_3 == 1: # Previous buffer is empty or next buffer is full
            Dosing_Speed = 0
        else:
            Dosing_Speed = 1500
            
        return Dosing_Speed
    
    def get_vp_4(self,Hopper_Filllevel_3,Silo_Filllevel_1):
        Saturator_4 = 0
        self.Hopper_Filllevel_3 = Hopper_Filllevel_3
        self.Silo_Filllevel_1 = Silo_Filllevel_1
        ##### Hopper -3 ######
        if self.Hopper_Filllevel_3 >=9.45:
            self.hopper_full_3 = 1 
        else:
            self.hopper_full_3 = 0

        if self.Hopper_Filllevel_3 < 1:
            self.hopper_empty_3 = 1
        else:
            self.hopper_empty_3 = 0
            
        ##### Silo-1 #######
            
        if self.Silo_Filllevel_1 >= 17.45:
            self.silo_full_1 = 1                # Here `1´ is signal for full
        else:
            self.silo_full_1 = 0

        if self.Silo_Filllevel_1 < 1:
            self.silo_empty_1 = 1               # Here `1´ is signal for empty 
        else:
            self.silo_empty_1 = 0
        
        ####### CONTROL FOR VA@4 #######
        
        if self.hopper_empty_3 == 1 or self.silo_full_1 == 1:    # Previous buffer is empty and next buffer is full
                Saturator_4 = 0
        else:
            Saturator_4 = 10
        return Saturator_4


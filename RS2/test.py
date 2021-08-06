# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 18:02:33 2021

@author: zj903545
"""
import keyboard as kb
import time
while True:
    try:
        if kb.is_pressed('1'): # move forward
            print("one")
            time.sleep(0.1)
        elif kb.is_pressed('2'): # move backwards
            print("two")
            time.sleep(0.1)
        elif kb.is_pressed('3'): # move backwards
            print("three")
            time.sleep(0.1)
        elif kb.is_pressed('q'): # quit
            break
        else:
            pass
    except:
        break  
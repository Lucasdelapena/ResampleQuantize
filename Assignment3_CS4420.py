# Lucas de la Pena
# CS4420
# Assignment 3
# 10/10/2024

import cv2
import numpy as np
import random
import os
import argparse
from screeninfo import get_monitors

#sample execution: python Assignment3_CS4420.py -s 2 -d 5 -i 3 imagefile

def check_args(s,d,i): #Arguments check
    if s < 1 or s > 2:
        print("Invalid sampling method. Please choose a number between 1 and 2.")
        return False
    
    if d < 1:
        print("Invalid depth. Please choose a number bigger than 0.")
        return False
    
    if i < 1 or i > 7:
        print("Invalid intensity. Please choose a number between 1 and 7.")
        return False
    
    return True

def main():
    # Arguments
    parser = argparse.ArgumentParser(prog='sample') # -h should be automatically added because of argparse
    parser.add_argument('-s', type=int, default=1, dest='sampling_Method')
    parser.add_argument('-d', type=int, default=1, dest='depth') 
    parser.add_argument('-i', type=int, default=1, dest='intensity')  
    parser.add_argument('imagefile', nargs='?')
    args = parser.parse_args()

    s = args.sampling_Method
    d = args.depth
    i = args.intensity

    if not check_args(s,d,i): #Arguments check
        return
    
    #Read image
    image = cv2.imread(args.imagefile)
    if image is None:
        print("Image not found.")
        return
    
    

    #Apply downsampling followed by upsampling




    
    
    

if __name__ == "__main__":
    main()
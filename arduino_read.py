import serial
import time
import numpy as np
# make sure the 'COM#' is set according the Windows Device Manager
ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
time.sleep(2)
from scamp import *
# from pynput import keyboard

# construct a session object
s = Session()
# add a new Piano part to the session
Sitar = s.new_part("Sitar")#Honky-tonk Piano")
Drum = s.new_part('Taiko Drum')
dur = 20
# key_map = {
#     'a': 50, # C
#     's': 55, # E
#     'd': 60, # G
# }
# 1->1semitone
# 52-> A-scale
keys_freq=[51,56,56,56]
drum_freq=[80,108]
flags=np.zeros(4)
flags_drum=np.zeros(2)
def on_press(key):
    for idx in range(key.shape[0]):
        # try:
        if key[idx]==0 and flags[idx]==1:
            flags[idx]=0
            continue
        if key[idx]==1 and flags[idx]==1: 
            continue
        if key[idx]==0 and flags[idx]==0:
            continue
        flags[idx]=1
        print(keys_freq[idx],key[idx])
        Sitar.play_note(keys_freq[idx],1.0,dur,blocking=False)
        
        # except:
            # pass
def play_drum(dist):
    for idx in range(dist.shape[0]):
        if dist[idx]<=thres_l:
            if flags_drum[idx]==1:
                continue
            print("TRUE!!!!!!")
            Drum.play_note(drum_freq[idx],1.0,dur,blocking=False)
            flags_drum[idx]=1
        elif dist[idx]>=thres_h:
            flags_drum[idx]=0
        
    
def extract_info():
    string = str(line)  # convert the byte string to a unicode string
    # print(string)
    str_vals=(string[2:-5].split(' '))
    try:
        int_val= np.array([eval(i) for i in str_vals])
    except:
        int_val=np.zeros(6)
    print(int_val)
    # num = int(string) # convert the unicode string to an int
    # print(num)
    if int_val.shape[0]!=6:
        return np.zeros(6)
    return int_val

prev_vals=np.zeros(2)
avg_pos=prev_vals
prev_time=time.time()
thres_l=8
thres_h=15
p=0
r_sum=0
while True:
    line = ser.readline()   # read a byte
    cur_time=time.time()
    if line:
        p+=1
        # string = line.decode()  # convert the byte string to a unicode string
        # num = int(string) # convert the unicode string to an int
        cur_vals=extract_info()
        on_press(cur_vals[2:])
        play_drum(cur_vals[:2])
        # print(num)

ser.close()


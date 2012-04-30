#! /usr/bin/env python
# synclient -m 20 | python syn_gesture.py
import sys
import os
#import compiz

def osd(msg):
    pass 

try:
    import pyosd
    osd=pyosd.osd()
    osd.set_offset(500)
    osd.set_outline_offset(2)
    osd=osd.display
except:
    print >> sys.stderr, ("no OSD")
    pass

def synsplit(line):
    result=[]
    d=line
    while True:
        d=d.lstrip()
        end=d.find(' ')
        if (end <0):
            result.append(d)
            return(result)
            break
        else:
            nextfield=d[0:end]
            d=d[end:len(d)]
            result.append(nextfield)
    return(result)

def str_for_delta(delta_x,delta_y):
    res_str=""
    if abs(delta_y)>150:
        if (delta_y<0): 
            res_str=res_str+"N"
        else:
            res_str=res_str+"S"
    if abs(delta_x)>150:
        if (delta_x<0): 
            res_str=res_str+"W"
        else:
            res_str=res_str+"E"
    return(res_str)

def main():
    sys.stdin.readline()
    last_pen_fingers=0
    touchpad=1
    old_osd_str=""
    while not sys.stdin.closed :
	line = sys.stdin.readline()
	ev=synsplit(line)
        if touchpad and ev[4]=="2": #fingers
         #   os.system("synclient Touchpadoff=1")
            touchpad=0
        if ev[4]=="2": #fingets
            try:
                c_delta_x=pen_x-begin_x
                c_delta_y=pen_y-begin_y
                osd_str=str_for_delta(c_delta_x,c_delta_y)
                #if old_osd_str!=osd_str:
                   #osd("["+osd_str+"]")
                old_osd_str=osd_str
            except:
                pass
        if ev[0]!="time":
            pen_x = int(ev[1])
            pen_y = int(ev[2])
            pen_fingers=int(ev[4])
            
        if (last_pen_fingers!=2) and (pen_fingers==2):
            begin_x=pen_x
            begin_y=pen_y
        if (last_pen_fingers==2) and (pen_fingers==0):
            delta_x=pen_x-begin_x
            delta_y=pen_y-begin_y
            res_str=str_for_delta(delta_x,delta_y)
            if res_str:
                print res_str + str(pen_fingers)
                #osd(res_str)
                if res_str=="W":
                    #compiz.call("rotate","rotate_right_key") 
                    print "evento W"
                if res_str=="E":
                    #compiz.call("rotate","rotate_left_key") 
                    print "evento E"
                if res_str=="S":
                    #compiz.call("widget","toggle_key") 
                    print "evento S"
                if res_str=="N":
                    #os.system("xset +dpms dpms force off") 
                    print "evento N"
        if (last_pen_fingers==3) and (pen_fingers==0):
            delta_x=pen_x-begin_x
            delta_y=pen_y-begin_y
            res_str=str_for_delta(delta_x,delta_y)
            if res_str:
                print res_str + str(pen_fingers)
                #osd(res_str)
                if res_str=="W":
                    #compiz.call("rotate","rotate_right_key") 
                    print "evento W3"
                if res_str=="E":
                    #compiz.call("rotate","rotate_left_key") 
                    print "evento E3"
                if res_str=="S":
                    #compiz.call("widget","toggle_key") 
                    print "evento S3"
                if res_str=="N":
                    #os.system("xset +dpms dpms force off") 
                    print "evento N3"
                    
        last_pen_fingers=pen_fingers
        #safety
        if (pen_fingers!=2):
            #os.system("synclient Touchpadoff=0")
            touchpad=1

if __name__ == '__main__':
    main()


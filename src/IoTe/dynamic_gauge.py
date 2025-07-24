#import all the modules needed
from math import *
import spidev
from time import sleep
from tkinter import *

#for reading ADC/potentiometer
spi=spidev.SpiDev()
spi.open(0,0)

#this is the initial value
pot_val=0 #0-1023
val=int(pot_val*100/1023) #0-100

#top frame or window
top=Tk()

#just add a pointer, and you will get a gauge!
gauge_img=PhotoImage(file="gauge.gif")

lowest=0 #gauge's lower limit
highest=100 #gauge's upper limit
start_x=128 #pointer's start x
start_y=145 #pointer's start y
leng=100 #pointer's length

#this will run every 500 ms
def update():
    #use the global variables declared earlier
    global pot_val
    global val

    #read the potentiometer value, scale it to 0-100
    spi.max_speed_hz=1350000
    r=spi.xfer2([1,8+0<<4,0]) #ADC ch 0
    pot_val=((r[1]&3)<<8)+r[2]
    val=int(pot_val*100/1023)

    #compute the pointer's andle, end x & y
    angle=pi*(val-lowest)/(highest-lowest) #measured clockwise from 9 o'clock position
    end_x=start_x-leng*cos(angle)
    end_y=start_y-leng*sin(angle)
    
    #redraw the gauge with new reading
    my_gauge.delete("all") #delete everything on canvas!
    my_gauge.create_image(0,0,image=gauge_img,anchor=NW) #add the background image
    my_gauge.create_line(start_x,start_y,end_x,end_y,fill="black",width=5) #add the pointer
    my_gauge.create_text(50,start_y+10,font="Arial 10",text=lowest) #add the lower limit
    my_gauge.create_text(216,start_y+10,font="Arial 10",text=highest) #add the upper limit
    my_gauge.create_text(start_x,start_y+50,font="Arial 20",text=val) #add the value
    
    #recursive, run once every 0.5 sec
    top.after(500,update)

#my gauge (a canvas) at column 0, row 0
my_gauge=Canvas(top,width=256,height=256) #width & height in pixels
my_gauge.grid(row=0,column=0) #more items can be added at different rows & columns

#set up the update to run first time:
top.after(0,update)

#main event loop
top.mainloop()










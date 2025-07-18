from sample_code import I2C_LCD_driver as LCD
from time import sleep

LCD = LCD.lcd() #instantiate an lcd object, call it LCD
LCD.backlight(1) #turn backlight on 
LCD.lcd_display_string("LCD Display Test", 1) #write on line 1
LCD.lcd_display_string("On", 2, 2) #write on line 2
sleep(2) #wait 2 sec
LCD.lcd_display_string("Off", 2)
sleep(2) #wait 2 sec
LCD.lcd_clear() #clear the display
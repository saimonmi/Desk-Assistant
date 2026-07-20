import time
import board
import digitalio
import usb_hid
import supervisor  
import sys
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


kbd = Keyboard(usb_hid.devices)


BUTTON_MAPPING = {
    board.GP12: Keycode.LEFT_ARROW,
    board.GP17: Keycode.RIGHT_ARROW,
    board.GP18: Keycode.UP_ARROW,
    board.GP13: Keycode.DOWN_ARROW,
    board.GP14: Keycode.RIGHT_SHIFT
}

configured_buttons = []
for pin, keycode in BUTTON_MAPPING.items():
    btn = digitalio.DigitalInOut(pin)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    configured_buttons.append((btn, keycode))

buzz=digitalio.DigitalInOut(board.GP16)
buzz.direction=digitalio.Direction.OUTPUT
buzz.value= True
last_states = {}
for btn, keycode in configured_buttons:
    last_states[btn] = btn.value


while True:
    for btn, keycode in configured_buttons:
        current_value = btn.value 
        if current_value != last_states[btn]:
            last_states[btn] = current_value  
            if current_value == True: 
                kbd.press(keycode)    
            else:
                kbd.release(keycode)    

    if supervisor.runtime.serial_bytes_available:
        befehl = sys.stdin.readline().strip()
        
        if befehl == "KLINGELN":
            for _ in range(3):
                buzz.value = False
                time.sleep(0.1)
                buzz.value = True
                time.sleep(0.1)   
    time.sleep(0.01)

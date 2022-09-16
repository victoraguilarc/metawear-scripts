from mbientlab.metawear import MetaWear, libmetawear
from mbientlab.metawear.cbindings import *
from time import sleep
from threading import Event

import sys


def connect_device():
    # connect
    # device = MetaWear('F9:BD:6E:48:2D:B0', hci_mac='00:1A:7D:DA:71:11')
    device = MetaWear('F9:BD:6E:48:2D:B0')
    device.connect()
    print("Connected to " + device.address + " over " + ("USB" if device.usb.is_connected else "BLE"))
    return device


def setup_led(device):
    # create led pattern
    pattern= LedPattern(repeat_count= Const.LED_REPEAT_INDEFINITELY)
    libmetawear.mbl_mw_led_load_preset_pattern(byref(pattern), LedPreset.BLINK)
    libmetawear.mbl_mw_led_write_pattern(device.board, byref(pattern), LedColor.GREEN)

    # play the pattern
    libmetawear.mbl_mw_led_play(device.board)

    # wait 5s
    sleep(5.0)


def clear_led(device):
    # remove the led pattern and stop playing
    libmetawear.mbl_mw_led_stop_and_clear(device.board)
    print("Done")
    sleep(5.0)

def reset_device(device):
    # Stops data logging
    libmetawear.mbl_mw_logging_stop(device.board)
    # Clear the logger of saved entries
    # libmetawear.mbl_mw_logging_clear_entries(device.board)
    # Remove all macros on the flash memory
    # libmetawear.mbl_mw_macro_erase_all(device.board)
    # Restarts the board after performing garbage collection
    libmetawear.mbl_mw_debug_reset_after_gc(device.board)
    print("Erase logger, state, and macros")
    libmetawear.mbl_mw_debug_disconnect(device.board)


def disconnect_device(device):
    # disconnect
    device.disconnect()
    sleep(5.0)


device = connect_device()
setup_led(device)
clear_led(device)
disconnect_device(device)

from mbientlab.warble import *
from mbientlab.metawear import *
from threading import Event
from mbientlab.metawear import MetaWear, libmetawear
from mbientlab.metawear.cbindings import *
import sys

# print('Starting')
# e = Event()
# address = None
# def device_discover_task(result):
#     global address
#     if (result.has_service_uuid(MetaWear.GATT_SERVICE)):
#         # grab the first discovered metawear device
#         address = result.mac
#         e.set()

# BleScanner.set_handler(device_discover_task)
# BleScanner.start()
# e.wait()

# BleScanner.stop()
# print(address)



# Where 'cb:7d:c5:b0:20:8f' = MAC address of MetaSensor
device = MetaWear('F9:BD:6E:48:2D:B0')
device.connect()




# Callback function to process/parse the gyroscope data
def data_handler(self, ctx, data):
    print("%s -> %s" % (self.device.address, parse_value(data)))


def subscribe():
    print('subscribing...')
    callback = FnVoid_VoidP_DataP(data_handler)

    # Setup the accelerometer sample frequency and range
    libmetawear.mbl_mw_acc_set_odr(device.board, 100.0)
    libmetawear.mbl_mw_acc_set_range(device.board, 16.0)
    libmetawear.mbl_mw_acc_write_acceleration_config(device.board)

    # Get the accelerometer data signal
    signal = libmetawear.mbl_mw_acc_get_acceleration_data_signal(device.board)
    # Subscribe to it
    libmetawear.mbl_mw_datasignal_subscribe(signal, None, callback)

    # Enable the accelerometer
    libmetawear.mbl_mw_acc_enable_acceleration_sampling(device.board)
    libmetawear.mbl_mw_acc_start(device.board)


subscribe()
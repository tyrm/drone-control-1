import asyncio
import logging
from Phidget22.Devices.DigitalOutput import *

runMin = 15
runMax = 60
sleepMin = 300
sleepMax = 60


class PopperPump:
    def __init__(self):
        logging.debug("Opening Phidget")
        self.popperPump = DigitalOutput()
        self.popperPump.setChannel(0)
        self.popperPump.openWaitForAttachment(5000)

        self.program_runnning = False
        self.program_lock = asyncio.Lock()
        self.run_time = 15  # 15 Seconds
        self.sleep_time = 600  # 10 Minutes

    def close(self):
        logging.debug("Closing Phidget")
        self.popperPump.close()

    def set_run(self, value):
        scale_value = int(((value * (runMax - runMin)) / 127) + runMin)
        #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        if self.run_time != scale_value:
            self.run_time = scale_value
            logging.debug("PopperPump run time set to %d seconds" % (scale_value, ))

    def set_sleep(self, value):
        scale_value = int(((value * (sleepMax - sleepMin)) / 127) + sleepMin)
        #NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

        if self.sleep_time != scale_value:
            self.sleep_time = scale_value
            logging.debug("PopperPump sleep time set to %d seconds" % (scale_value, ))

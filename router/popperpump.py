import threading, queue
import logging
from Phidget22.Devices.DigitalOutput import *

runMin = 15
runMax = 60
sleepMin = 300
sleepMax = 60


class PopperPump:
    def __init__(self, serial):
        logging.debug("Opening Phidget")
        self.popperPump = DigitalOutput()
        self.popperPump.setChannel(0)
        self.popperPump.setDeviceSerialNumber(serial)
        self.popperPump.openWaitForAttachment(5000)

        self.program_lock = threading.Lock()
        self.program_queue = queue.Queue()
        self.run_time = 15  # 15 Seconds
        self.sleep_time = 600  # 10 Minutes

    def close(self):
        logging.debug("Closing Phidget")
        self.popperPump.close()

    def is_program_running(self):
        return self.program_lock.locked()

    def program(self):
        if not self.program_lock.acquire(False):
            logging.warning("popperpump program already running")
        else:
            logging.info("starting popperpump program")
            try:
                while True:
                    self.popperPump.setDutyCycle(0)
                    try:
                        msg = self.program_queue.get(timeout=self.sleep_time)
                        # Message Received
                        self.popperPump.setDutyCycle(0)
                        return
                    except queue.Empty:
                        pass

                    self.popperPump.setDutyCycle(1)
                    try:
                        msg = self.program_queue.get(timeout=self.run_time)
                        # Message Received
                        self.popperPump.setDutyCycle(0)
                        return
                    except queue.Empty:
                        pass
            finally:
                logging.info("popperpump program stopped")
                self.program_lock.release()

    def set_run(self, value):
        scale_value = int(((value * (runMax - runMin)) / 127) + runMin)
        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
        if self.run_time != scale_value:
            self.run_time = scale_value
            logging.debug("PopperPump run time set to %d seconds" % (scale_value,))

    def set_sleep(self, value):
        scale_value = int(((value * (sleepMax - sleepMin)) / 127) + sleepMin)
        # NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin

        if self.sleep_time != scale_value:
            self.sleep_time = scale_value
            logging.debug("PopperPump sleep time set to %d seconds" % (scale_value,))

    def start_program(self):
        threading.Thread(target=self.program, daemon=True).start()

    def stop_program(self):
        self.program_queue.put("stop")

import logging
import queue
import threading

from Phidget22.Devices.DigitalOutput import *

import util
from kontrol2 import Kontrol2, KontrolAlreadyAttachedError, KontrolNotAttachedError

runMin = 10
runMax = 30
sleepMin = 300
sleepMax = 60

class PopperPump:
    def __init__(self, serial_num):
        logging.debug("Opening Phidget")
        self.popper_pump = DigitalOutput()
        self.popper_pump.setChannel(0)
        self.popper_pump.setDeviceSerialNumber(serial_num)
        self.popper_pump.openWaitForAttachment(5000)

        self.program_lock = threading.Lock()
        self.program_queue = queue.Queue()
        self.run_time = runMin
        self.sleep_time = sleepMin

        # Required for Kontroller
        self.kontrol = None
        self.channel = None

    def close(self):
        logging.debug("Closing Phidget")
        self.popper_pump.close()

    def program_is_running(self):
        return self.program_lock.locked()


    def set_run(self, value):
        if self.run_time != value:
            self.run_time = value
            logging.debug(f'PopperPump run time set to {value} seconds')

    def set_sleep(self, value):
        if self.sleep_time != value:
            self.sleep_time = value
            logging.debug(f'PopperPump sleep time set to {value} seconds')

    def start_program(self):
        threading.Thread(target=self._program, daemon=True).start()

    def stop_program(self):
        self.program_queue.put("stop")

    # Private Functions
    def _program(self):
        if not self.program_lock.acquire(False):
            logging.warning("popperpump program already running")
        else:
            logging.info("starting popperpump program")
            try:
                while True:
                    self.popper_pump.setDutyCycle(1)
                    self.kontrol.k_led_on(self.channel, 's')
                    try:
                        msg = self.program_queue.get(timeout=self.run_time)
                        # Message Received
                        self.popper_pump.setDutyCycle(0)
                        self.kontrol.k_led_off(self.channel, 's')
                        return
                    except queue.Empty:
                        pass

                    self.popper_pump.setDutyCycle(0)
                    self.kontrol.k_led_off(self.channel, 's')
                    try:
                        msg = self.program_queue.get(timeout=self.sleep_time)
                        # Message Received
                        self.popper_pump.setDutyCycle(0)
                        self.kontrol.k_led_off(self.channel, 's')
                        return
                    except queue.Empty:
                        pass
            finally:
                logging.info("popperpump program stopped")
                self.program_lock.release()

    # Kontrol Functions
    def k_attach(self, channel, k: Kontrol2):
        if self.kontrol is None:
            self.kontrol = k
            self.channel = channel
            logging.debug(f'PopperPump attached on channel {channel}')
        else:
            raise KontrolAlreadyAttachedError(f'cannot attach to channel {channel} already attached to {self.channel}')

    def k_button_down(self, button, ):
        if button == 'r':
            if self.kontrol is not None:
                if self.program_is_running():
                    self.stop_program()
                    self.kontrol.k_led_off(self.channel, 'r')
                else:
                    self.start_program()
                    self.kontrol.k_led_on(self.channel, 'r')
        else:
            raise KontrolNotAttachedError(f'PopperPump not attached to Kontroller')

    def k_button_up(self, button):
        if self.kontrol is not None:
            pass # Unused
        else:
            raise KontrolNotAttachedError(f'PopperPump not attached to Kontroller')

    def k_knob(self, level):
        if self.kontrol is not None:
            scale_level = int(util.scale(level, (0, 127), (sleepMin, sleepMax)))
            self.set_sleep(scale_level)
        else:
            raise KontrolNotAttachedError(f'PopperPump not attached to Kontroller')

    def k_slider(self, level):
        if self.kontrol is not None:
            scale_level = int(util.scale(level, (0, 127), (runMin, runMax)))
            self.set_run(scale_level)
        else:
            raise KontrolNotAttachedError(f'PopperPump not attached to Kontroller')
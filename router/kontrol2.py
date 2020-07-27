import constant  # local
import logging
import mido


class Kontrol2:
    def __init__(self, pp):

        # Connect to
        logging.debug("Input Ports {}".format(mido.get_input_names()))
        self.inport = mido.open_input('nanoKONTROL2:nanoKONTROL2 MIDI 1 32:0', callback=self.midiCallback)
        logging.debug("Output Ports {}".format(mido.get_output_names()))
        self.outport = mido.open_output('nanoKONTROL2:nanoKONTROL2 MIDI 1 32:0')

        self.popperpump = pp


    def close(self):
        self.popperpump.close()

        self.inport.close()
        self.outport.close()

    def ledOn(self, led):
        msgOn = mido.Message('control_change', control=led, value=127)
        self.outport.send(msgOn)

    def midiCallback(self, message):
        control = message.control
        value = message.value
        if (control in constant.BUTTONS):
            name = constant.BUTTONS[control]
            if (value == 127):
                return self.buttonDown(name)
            else:
                return self.buttonUp(name)
        else:
            try:
                idx = constant.KNOBS.index(control)
                return self.twistedKnob(idx, value)
            except ValueError:
                pass
            try:
                idx = constant.SLIDERS.index(control)
                return self.slidSlider(idx, value)
            except ValueError:
                pass

            print("Control: %d, Value: %d" % (control, value))
        print(message)

    def buttonDown(self, button):
        if button == 'r_0':
            # PopperPump Toggle Run
            if self.popperpump.is_program_running():
                self.popperpump.stop_program()
            else:
                self.popperpump.start_program()
        else:
            logging.debug("Pushed button %s" % (button,))

    def buttonUp(self, button):
        logging.debug("Released button %s" % (button,))

    def twistedKnob(self, idx, value):
        if idx == 0:
            self.popperpump.set_sleep(value)
        else:
            logging.debug("Twisted knob %d to %d" % (idx, value))

    def slidSlider(self, idx, value):
        if idx == 0:
            self.popperpump.set_run(value)
        else:
            logging.debug("Slid slider %d to %d" % (idx, value))

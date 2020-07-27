import constant  # local
import logging
import mido


class Kontrol2:
    def __init__(self, pp):

        # Connect to
        logging.debug("Input Ports {}".format(mido.get_input_names()))
        self.inport = mido.open_input('nanoKONTROL2:nanoKONTROL2 MIDI 1 32:0', callback=self.midi_callback)
        logging.debug("Output Ports {}".format(mido.get_output_names()))
        self.outport = mido.open_output('nanoKONTROL2:nanoKONTROL2 MIDI 1 32:0')

        self.popperpump = pp

    def close(self):
        self.popperpump.close()

        self.inport.close()
        self.outport.close()

    def led_off(self, led):
        msgOn = mido.Message('control_change', control=led, value=0)
        self.outport.send(msgOn)

    def led_on(self, led):
        msgOn = mido.Message('control_change', control=led, value=127)
        self.outport.send(msgOn)

    def midi_callback(self, message):
        control = message.control
        value = message.value
        if (control in constant.BUTTONS):
            name = constant.BUTTONS[control]
            if (value == 127):
                return self.button_down(name)
            else:
                return self.button_up(name)
        else:
            try:
                idx = constant.KNOBS.index(control)
                return self.twisted_knob(idx, value)
            except ValueError:
                pass
            try:
                idx = constant.SLIDERS.index(control)
                return self.slid_slider(idx, value)
            except ValueError:
                pass

            print("Control: %d, Value: %d" % (control, value))
        print(message)

    def button_down(self, button):
        if button == 'r_0':
            # PopperPump Toggle Run
            if self.popperpump.is_program_running():
                self.popperpump.stop_program()
                self.led_off(constant.BUTTON_R_0)
            else:
                self.popperpump.start_program()
                self.led_on(constant.BUTTON_R_0)
        else:
            logging.debug("Pushed button %s" % (button,))

    def button_up(self, button):
        logging.debug("Released button %s" % (button,))

    def twisted_knob(self, idx, value):
        if idx == 0:
            self.popperpump.set_sleep(value)
        else:
            logging.debug("Twisted knob %d to %d" % (idx, value))

    def slid_slider(self, idx, value):
        if idx == 0:
            self.popperpump.set_run(value)
        else:
            logging.debug("Slid slider %d to %d" % (idx, value))

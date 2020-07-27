import logging
import mido

BUTTONS = {
    58: 'track_left',
    59: 'track_right',
    46: 'cycle',
    60: 'marker_set',
    61: 'marker_left',
    62: 'marker_right',
    43: 'rwd',
    44: 'fwd',
    42: 'stop',
    41: 'play',
    45: 'record',
    32: 's_0',
    33: 's_1',
    34: 's_2',
    35: 's_3',
    36: 's_4',
    37: 's_5',
    38: 's_6',
    39: 's_7',
    48: 'm_0',
    49: 'm_1',
    50: 'm_2',
    51: 'm_3',
    52: 'm_4',
    53: 'm_5',
    54: 'm_6',
    55: 'm_7',
    64: 'r_0',
    65: 'r_1',
    66: 'r_2',
    67: 'r_3',
    68: 'r_4',
    69: 'r_5',
    70: 'r_6',
    71: 'r_7'
}

KNOBS = [16, 17, 18, 19, 20, 21, 22, 23]

SLIDERS = [0, 1, 2, 3, 4, 5, 6, 7]

LEDS = {
    'track_left': 58,
    'track_right': 59,
    'cycle': 46,
    'marker_set': 60,
    'marker_left': 61,
    'marker_right': 62,
    'rwd': 43,
    'fwd': 44,
    'stop': 42,
    'play': 41,
    'record': 45,
    's_0': 32,
    's_1': 33,
    's_2': 34,
    's_3': 35,
    's_4': 36,
    's_5': 37,
    's_6': 38,
    's_7': 39,
    'm_0': 48,
    'm_1': 49,
    'm_2': 50,
    'm_3': 51,
    'm_4': 52,
    'm_5': 53,
    'm_6': 54,
    'm_7': 55,
    'r_0': 64,
    'r_1': 65,
    'r_2': 66,
    'r_3': 67,
    'r_4': 68,
    'r_5': 69,
    'r_6': 70,
    'r_7': 71
}

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
        msgOn = mido.Message('control_change', control=LEDS[led], value=0)
        self.outport.send(msgOn)

    def led_on(self, led):
        msgOn = mido.Message('control_change', control=LEDS[led], value=127)
        self.outport.send(msgOn)

    def midi_callback(self, message):
        control = message.control
        value = message.value
        if (control in BUTTONS):
            name = BUTTONS[control]
            if (value == 127):
                return self.button_down(name)
            else:
                return self.button_up(name)
        else:
            try:
                idx = KNOBS.index(control)
                return self.twisted_knob(idx, value)
            except ValueError:
                pass
            try:
                idx = SLIDERS.index(control)
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
                self.led_off('r_0')
            else:
                self.popperpump.start_program()
                self.led_on('r_0')
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

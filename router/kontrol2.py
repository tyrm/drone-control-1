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
    'track_left':   58,
    'track_right':  59,
    'cycle':        46,
    'marker_set':   60,
    'marker_left':  61,
    'marker_right': 62,
    'rwd':          43,
    'fwd':          44,
    'stop':         42,
    'play':         41,
    'record':       45,
    's_0':          32,
    's_1':          33,
    's_2':          34,
    's_3':          35,
    's_4':          36,
    's_5':          37,
    's_6':          38,
    's_7':          39,
    'm_0':          48,
    'm_1':          49,
    'm_2':          50,
    'm_3':          51,
    'm_4':          52,
    'm_5':          53,
    'm_6':          54,
    'm_7':          55,
    'r_0':          64,
    'r_1':          65,
    'r_2':          66,
    'r_3':          67,
    'r_4':          68,
    'r_5':          69,
    'r_6':          70,
    'r_7':          71
}


class Kontrol2:
    def __init__(self, port):

        # Connect to
        logging.debug(f'Input Ports {mido.get_input_names()}')
        self.inport = mido.open_input(port, callback=self._midi_callback)
        logging.debug(f'Output Ports {mido.get_output_names()}')
        self.outport = mido.open_output(port)

        self.control_objects = [GenericKontrol(), GenericKontrol(), GenericKontrol(), GenericKontrol(),
                                GenericKontrol(), GenericKontrol(), GenericKontrol(), GenericKontrol()]

    def close(self):
        self.inport.close()
        self.outport.close()

    def led_off(self, led):
        msgOn = mido.Message('control_change', control=LEDS[led], value=0)
        self.outport.send(msgOn)

    def led_on(self, led):
        msgOn = mido.Message('control_change', control=LEDS[led], value=127)
        self.outport.send(msgOn)

    # Kontrol Object functions
    def k_led_on(self, led, channel):
        msgOn = mido.Message('control_change', value=127)

        if led == 's':
            msgOn.control = LEDS['s_0'] + channel
        elif led == 'm':
            msgOn.control = LEDS['m_0'] + channel
        elif led == 'r':
            msgOn.control = LEDS['r_0'] + channel
        else:
            logging.error(f'Got invalid led [{led}] on channel {channel}')
            return

        self.outport.send(msgOn)

    # Privates
    def _midi_callback(self, message):
        control = message.control
        value = message.value
        if (control in BUTTONS):
            if (value == 127):
                return self._button_down(control)
            else:
                return self._button_up(control)
        else:
            try:
                idx = KNOBS.index(control)
                return self._twisted_knob(idx, value)
            except ValueError:
                pass
            try:
                idx = SLIDERS.index(control)
                return self._slid_slider(idx, value)
            except ValueError:
                pass

            print("Control: %d, Value: %d" % (control, value))
        print(message)

    def _button_down(self, button):
        if 32 <= button <= 39:
            # s button
            channel = button - 32
            self.control_objects[channel].k_button_down(channel, 's', self)
        if 48 <= button <= 55:
            # m button
            channel = button - 48
            self.control_objects[channel].k_button_down(channel, 'm', self)
        if 64 <= button <= 71:
            # r button
            channel = button - 64
            self.control_objects[channel].k_button_down(channel, 'r', self)

    def _button_up(self, button):
        if 32 <= button <= 39:
            # s button
            channel = button - 32
            self.control_objects[channel].k_button_up(channel, 's', self)
        if 48 <= button <= 55:
            # m button
            channel = button - 48
            self.control_objects[channel].k_button_up(channel, 'm', self)
        if 64 <= button <= 71:
            # r button
            channel = button - 64
            self.control_objects[channel].k_button_up(channel, 'r', self)

    def _twisted_knob(self, idx, value):
        self.control_objects[idx].k_knob(idx, value, self)

    def _slid_slider(self, idx, value):
        self.control_objects[idx].k_slider(idx, value, self)


class GenericKontrol:
    def __init__(self):
        self.slider = 0
        self.knob = 0

        self.running = False

    def k_button_down(self, channel, button, k: Kontrol2):
        logging.debug(f'Pushed button {button}_{channel}')

        if button == 'r':
            if self.running:
                self.running = False
            else:
                self.running = True

    def k_button_up(self, channel, button, k: Kontrol2):
        logging.debug(f'Released button {button}_{channel}')

        if button == 'r':
            if self.running:
                self.running = False
            else:
                self.running = True

    def k_knob(self, channel, level, k: Kontrol2):
        logging.debug(f'Twisted knob {channel} to {level}')
        self.knob = level

    def k_slider(self, channel, level, k: Kontrol2):
        logging.debug(f'Slid slider {channel} to {level}')
        self.slider = level

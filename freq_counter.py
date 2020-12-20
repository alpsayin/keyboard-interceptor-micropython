import time
from machine import Pin
from micropython import const
import array
from uart_wrapper import DEFAULT_BAUDRATE

NUM_SAMPLES = const(8)


def _freq_counter_irq_falling(fc, pin_obj):
    now_us = time.ticks_us()
    fc.period_samples[fc.list_idx] = time.ticks_diff(now_us, fc.last_ticks_us)
    fc.list_idx = (fc.list_idx + 1) % NUM_SAMPLES
    fc.last_ticks_us = now_us

class FreqCounter():
    def __init__(self, pin_number):
        # super().__init__()
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.last_ticks_us = 0
        self.period_us = int(1000000/DEFAULT_BAUDRATE)
        self.period_samples = array.array('L', [self.period_us] * NUM_SAMPLES)
        self.freq_hz = int(1/self.period_us)
        self.list_idx = 0
        self.pin.irq(
            trigger=Pin.IRQ_FALLING,
            handler=lambda pin_obj: _freq_counter_irq_falling(self, pin_obj)
        )

    def average_samples(self):
        self.period_us = sum(self.period_samples) / NUM_SAMPLES
        # print('{} periods {}'.format(self.pin, self.period_samples))
        self.freq_hz = 1000000/self.period_us

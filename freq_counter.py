import time
from machine import Pin
from micropython import const


def _freq_counter_irq_falling(fc, pin_obj):
    now_us = time.ticks_us()
    fc.ticks_delta = time.ticks_diff(now_us, fc.last_ticks_us)
    fc.period_us = fc.ticks_delta
    fc.freq_hz = round(1000000/fc.period_us)
    print('{} freq {}'.format(pin_obj, fc.freq_hz))
    fc.last_ticks_us = now_us


class FreqCounter():
    def __init__(self, pin_number):
        # super().__init__()
        self.pin = Pin(pin_number, Pin.IN)
        self.last_ticks_us = 0
        self.period_us = 0
        self.freq_hz = 10000
        self.pin.irq(
            trigger=Pin.IRQ_FALLING,
            handler=lambda pin_obj: _freq_counter_irq_falling(self, pin_obj)
        )


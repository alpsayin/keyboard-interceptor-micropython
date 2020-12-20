import machine
from machine import UART
from micropython import const

TX_PIN = const(26)
RX_PIN = const(27)
BAUD_R5 = const(115200)
BAUD_R8 = const(921600)
TXBUF_LEN = const(256)
RXBUF_LEN = const(256)
READ_TIMEOUT = 0  # timeout specifies the time to wait for the first character (ms)
WRITE_WAIT = 0  # timeout_char specifies the time to wait between characters (ms)

raw_uart = None
baudrate = BAUD_R8


def update_baudrate(new_baudrate):
    global raw_uart, baudrate
    raw_uart.deinit()
    baudrate = int(round(new_baudrate))
    init()


def init():
    global raw_uart, baudrate
    raw_uart = UART(1, tx=TX_PIN, rx=RX_PIN)
    raw_uart.init(
        baudrate=baudrate,
        bits=8,
        parity=None,
        stop=1,
        tx=TX_PIN,
        rx=RX_PIN,
        txbuf=TXBUF_LEN,
        rxbuf=RXBUF_LEN,
        timeout=READ_TIMEOUT,
        timeout_char=WRITE_WAIT
    )
    raw_uart.write('\r\n# UART initialised\r\n')
    return raw_uart

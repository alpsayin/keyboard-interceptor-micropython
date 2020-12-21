import time


def wait(wait_time):
    print('Press CTRL-C in {} seconds to drop to REPL'.format(wait_time), end='')
    for seconds in range(wait_time):
        print('\rPress CTRL-C in {} seconds to drop to REPL'.format(wait_time-seconds), end='')
        print('.' * (seconds+1), end='')
        time.sleep(1)
    print('\rPress CTRL-C in 0 seconds to drop to REPL%s' % ('.' * wait_time))

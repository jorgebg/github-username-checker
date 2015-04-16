ENABLED = True

HEADER = '\033[95m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

def color(c):
    if ENABLED:
        return lambda x: '{0}{1}{2}'.format(c,x,ENDC)
    return lambda x: '{}'.format(x)

header = color(HEADER)
green = color(OKGREEN)
warn = color(WARNING)
fail = color(FAIL)

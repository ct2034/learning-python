from terminalplot import plot
from math import sin, pi

x = range(1000)
y = [sin(i / 1000 * 2 * pi) for i in x]
plot(x, y, rows=40, columns=80)

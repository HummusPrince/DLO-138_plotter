from serial import Serial as ser
from time import sleep
import matplotlib.pyplot as plt


p = ser('COM3', 115200)

print("Waiting for data.")

while p.in_waiting == 0:
    sleep(0.25)

print("Acquiring...")

while True:
    tmp = p.in_waiting
    sleep(0.1)
    if tmp == p.in_waiting:
        break

t = p.read_all().split(b'\r\n')
ch1 = [float(i.split(b'\t')[1]) for i in t[12:-2]]

plt.plot(ch1)
plt.show()

p.close()
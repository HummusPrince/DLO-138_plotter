from serial import Serial as ser
from time import sleep
import matplotlib.pyplot as plt


def acquire(comport = 'COM3'):

    p = ser(comport, 115200)

    print("Waiting for data.")

    while p.in_waiting == 0:
        sleep(0.25)

    print("Acquiring...")

    while True:
        tmp = p.in_waiting
        sleep(0.1)
        if tmp == p.in_waiting:
            break
            
    acquisition = [str(line, 'ascii') for line in p.read_all().split(b'\r\n')]
    
    p.close()
    
    print("Done")
    
    return acquisition
    
    
def parse(lines):
    
    plotdict = dict()
    #plotdict['Tscale'] = float(lines[2].split()[1])
    plotdict ['TscaleUnits'] = lines[2].split()[2][:2]
    plotdict['Tscale'] = float(lines[3].split()[-1])
    if plotdict['TscaleUnits'] == 'mS':
        plotdict['Tscale'] /= 1000
    plotdict['coupling'] = lines[4].split()[2]
    plotdict['Vscale'] = lines[4].split()[4]
    plotdict['VscaleUnits'] = 'mV' if plotdict['Vscale'][-6] == 'm' else 'V'
    plotdict['ch1'] = [float(i.split('\t')[1]) for i in lines[12:-2]]
    plotdict['VoltageStats'] = lines[8].strip().replace(', ','\n')
    plotdict['SignalStats'] = lines[9].strip().replace(', ','\n')
    
    assert len(plotdict['ch1']) == 2048
    
    return plotdict
    
    
def plot(plotdict):
    plt.style.use('dark_background')
    plt.plot([i * plotdict['Tscale']/25 for i in range(2048)], plotdict['ch1'], color = '#FFFF00', linewidth = 0.1, antialiased = False)
    plt.grid(color = '#404040', linewidth = 1, antialiased = True)
    plt.xlabel('Time [{}]'.format(plotdict['TscaleUnits']))
    plt.ylabel('Voltage [{}]'.format(plotdict['VscaleUnits']))
    tmpaxis = list(plt.axis())
    tmpaxis[3] += (tmpaxis[3] - tmpaxis[2])*0.3
    plt.axis(tmpaxis)

    plt.text(tmpaxis[1]*0.95, tmpaxis[3]*0.95, plotdict['VoltageStats'], fontsize = 8, ha = 'right', va = 'top', ma = 'left')
    plt.text(0, tmpaxis[3]*0.95, plotdict['SignalStats'], fontsize = 8, ha = 'left', va = 'top', ma = 'left')
    plt.show()

    
if __name__ == "__main__":
    #plot(parse(acquire()))
    plotdict = parse(acquire('COM3'))
    plot(plotdict)
    #pass
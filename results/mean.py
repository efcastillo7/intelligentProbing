# ==========================
import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
import csv as csv
import numpy as np
import matplotlib.pyplot as plt

def ReadCSV(csv_file,csv_function='r'):
    x = []
    y = []
    z = []
    speed_tx_mean=speed_rx_mean=speed_tx_std=speed_rx_std=0
    
    with open(csv_file, csv_function) as csvfile:
        plots = csv.DictReader(csvfile)
        for row in plots:
                x.append(int(row["Row"]))
                y.append(int(row["TX"]))
                z.append(int(row["RX"]))
    
        speed_tx_mean = Bytes_to(np.mean(y))
        speed_rx_mean = Bytes_to(np.mean(z))

        speed_tx_std = Bytes_to(np.std(y))
        speed_rx_std = Bytes_to(np.std(z))

    return [speed_tx_mean, speed_rx_mean, speed_tx_std, speed_rx_std]


f_05 = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_05s/speed_05.csv")
f_1  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_1s/speed_1.csv")
f_2  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_2s/speed_2.csv")
f_3  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_3s/speed_3.csv")
f_4  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_4s/speed_4.csv")

f_5  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_4s/speed_4.csv")

f_6  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_6s/speed_6.csv")
f_7  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_7s/speed_7.csv")
f_10  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_10s/speed_10.csv")
f_15  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_15s/speed_15.csv")
f_20  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_20s/speed_20.csv")
f_25  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_25s/speed_25.csv")
f_30  = ReadCSV("/home/efcastillo/ryu/ryu/app/intelligentProbing/results/probing_30s/speed_30.csv")


frequencies = ['TX', 'RX']
x_pos = np.arange(len(frequencies))

CTEs = [f_5[0], f_5[1]]
error = [f_5[2], f_5[3]]


# Build the plot
fig, ax = plt.subplots()
ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
ax.set_ylabel('Control channel load')
ax.set_xticks(x_pos)
ax.set_xticklabels(frequencies)
ax.set_title('Title')
ax.yaxis.grid(True)

# Save the figure and show
plt.tight_layout()
#plt.savefig('bar_plot_with_error_bars.png')
plt.show()
###########################################################################################
import matplotlib.pyplot as plt
import numpy as np

data_a = [[1,2,5], [5,7,2,2,5], [7,2,5]]
data_b = [[6,4,2], [1,2,5,3,2], [2,3,5,1]]

ticks = ['A', 'B', 'C']

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)

plt.figure()

bpl = plt.boxplot(data_a, positions=np.array(range(len(data_a)))*2.0-0.4, sym='', widths=0.6)
bpr = plt.boxplot(data_b, positions=np.array(range(len(data_b)))*2.0+0.4, sym='', widths=0.6)
set_box_color(bpl, '#D7191C') # colors are from http://colorbrewer2.org/
set_box_color(bpr, '#2C7BB6')

# draw temporary red and blue lines and use them to create a legend
plt.plot([], c='#D7191C', label='Apples')
plt.plot([], c='#2C7BB6', label='Oranges')
plt.legend()

plt.xticks(range(0, len(ticks) * 2, 2), ticks)
plt.xlim(-2, len(ticks)*2)
plt.ylim(0, 8)
plt.tight_layout()
#plt.show()
###########################################################################################
import matplotlib.pyplot as plt
import numpy as np
import random

data = {}
data['dataset1'] = {}
data['dataset2'] = {}
data['dataset3'] = {}

n = 500
for k,v in data.items():
    upper = random.randint(0, 1000)
    v['A'] = np.random.uniform(0, upper, size=n)
    v['B'] = np.random.uniform(0, upper, size=n)
    v['C'] = np.random.uniform(0, upper, size=n)

fig, axes = plt.subplots(ncols=3, sharey=True)
fig.subplots_adjust(wspace=0)

for ax, name in zip(axes, ['dataset1', 'dataset2', 'dataset3']):
    ax.boxplot([data[name][item] for item in ['A', 'B', 'C']])
    ax.set(xticklabels=['A', 'B', 'C'], xlabel=name)
    ax.margins(0.05) # Optional

#plt.show()

# http://pythonforundergradengineers.com/python-matplotlib-error-bars.html
# https://plot.ly/create/?fid=tarzzz:1204#/
# https://matplotlib.org/gallery/units/bar_unit_demo.html
# https://chrisalbon.com/python/data_visualization/matplotlib_grouped_bar_plot/
# Barras http://blog.topspeedsnail.com/archives/724

fig = plt.figure(0)
x = np.arange(10.0)
y = np.sin(np.arange(10.0) / 20.0 * np.pi)

plt.errorbar(x, y, yerr=0.1)

y = np.sin(np.arange(10.0) / 20.0 * np.pi) + 1
plt.errorbar(x, y, yerr=0.1, uplims=True)

y = np.sin(np.arange(10.0) / 20.0 * np.pi) + 2
upperlimits = np.array([1, 0] * 5)
lowerlimits = np.array([0, 1] * 5)
plt.errorbar(x, y, yerr=0.1, uplims=upperlimits, lolims=lowerlimits)

plt.xlim(-1, 10)

###############################################################################

fig = plt.figure(1)
x = np.arange(10.0) / 10.0
y = (x + 0.1)**2

plt.errorbar(x, y, xerr=0.1, xlolims=True)
y = (x + 0.1)**3

plt.errorbar(x + 0.6, y, xerr=0.1, xuplims=upperlimits, xlolims=lowerlimits)

y = (x + 0.1)**4
plt.errorbar(x + 1.2, y, xerr=0.1, xuplims=True)

plt.xlim(-0.2, 2.4)
plt.ylim(-0.1, 1.3)

plt.show()

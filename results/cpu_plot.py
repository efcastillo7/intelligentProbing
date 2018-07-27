import matplotlib.pyplot as plt
import csv

x = []
y = []
z = []

with open('cpu_usage_001.csv','r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(float(row["TIME"]))
        y.append(float(row["CPU"]))
        z.append(float(row["REAL_MB"]))

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

ax.plot(x, y, '-', lw=1, color='r')

ax.set_ylabel('CPU (%)', color='r')
ax.set_xlabel('time (s)')
ax.set_ylim(0., max(y) * 1.2)

ax2 = ax.twinx()

ax2.plot(x, z, '-', lw=1, color='b')
ax2.set_ylim(0., max(z) * 1.2)

ax2.set_ylabel('Real Memory fer (MB)', color='b')

ax.grid()

#fig.savefig(plot)
plt.show()

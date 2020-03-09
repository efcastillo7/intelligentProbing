import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np


blue_data = [38.3,32.4,27.3,20.6,11.7,10.1,8.2,8.7,8.7,8.2,8.1,8.7,7.7,7.1,6.1]
red_data = [15008,11103,8665,5292,2705,2083,1829,1477,1470,1434,1413,1327,1201,991,906]


width = 0.2 # the width of a bar
# red dashes, blue squares and green triangles
f, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
plt.plot(red_data, blue_data, '^', color="black")
legend = ['CUC with the monitoring process']
plt.legend(legend, loc="upper right", fontsize=18)
plt.sca(ax2)
ax2.set_ylabel('CUC (%)', fontsize=26)
ax2.set_xlabel('Number of Read-State Reply Messages', fontsize=26)
ax2.tick_params(axis='x', direction='out', labelsize=26, labelrotation=45)
ax2.tick_params(axis='y', direction='out', labelsize=26)

plt.ylim([0., 100])
plt.xlim(0, 16000)

plt.tight_layout()
plt.grid()
plt.show()
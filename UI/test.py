import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
gs1 = gridspec.GridSpec(3, 3)
gs1.update(wspace=0.5, hspace=0.1)
for i in range(9):
    ax1 = plt.subplot(gs1[i])
    ax1.set_aspect('equal')
plt.show()
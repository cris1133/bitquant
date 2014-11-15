import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cPickle as pickle
from matplotlib import rcParams

def pickleLoader(pklFile):
    try:
        while True:
            yield pickle.load(pklFile)
    except EOFError:
        pass

def animate(i):
    bids = np.array([[float(price[0]), float(price[1])] for price in data[i]['bids']])
    asks = np.array([[float(price[0]), float(price[1])] for price in data[i]['asks']])
    x_bids=bids[:25,0]
    y_bids=bids[:25,1].cumsum()
    x_asks=asks[:25,0]
    y_asks=asks[:25,1].cumsum()
    price = float(data[i]['ticker'][u'last'])
    line.set_data(x_bids, y_bids)  # update the data
    line2.set_data(x_asks,y_asks)
    price_line.set_xdata(price)
    return line,line2,price_line

#Init only required for blitting to give a clean slate.
def init():
    line.set_ydata(np.ma.array(np.arange(25), mask=True))
    line2.set_ydata(np.ma.array(np.arange(25), mask=True))
    price_line.set_xdata(0.0)
    return line,line2,price_line

rcParams['figure.figsize'] = (8, 4)
rcParams['figure.dpi'] = 150
#rcParams['axes.color_cycle'] = dark2_colors
rcParams['lines.linewidth'] = 2
rcParams['axes.grid'] = True
#rcParams['axes.facecolor'] = '#eeeeee'
rcParams['font.size'] = 14
rcParams['patch.edgecolor'] = 'none'

data = {}
filename = "test.p"
with open(filename) as f:
    for i,event in enumerate(pickleLoader(f)):
        #print event['time']
        data[i] = event

fig, ax = plt.subplots()
ax.set_ylim(0,500)
ax.set_xlim(388,398)
ax.set_title("Bitstamp Order Book")
ax.set_xlabel("Price ($)")
ax.set_ylabel("Volume (cumulative)")

bids = np.array([[float(price[0]), float(price[1])] for price in data[0]['bids']])
asks = np.array([[float(price[0]), float(price[1])] for price in data[0]['asks']])

x_bids=bids[:25,0]
y_bids=bids[:25,1].cumsum()
x_asks=asks[:25,0]
y_asks=asks[:25,1].cumsum()

price = float(data[0]['ticker'][u'last'])

#x = np.arange(0, 2*np.pi, 0.01)        # x-array
line,line2,price_line = ax.plot(x_bids, y_bids)[0],ax.plot(x_asks, y_asks)[0], ax.axvline(price,ls='--')



ani = animation.FuncAnimation(fig, animate, np.arange(1, len(data)), init_func=init,
    interval=100, blit=True)


plt.show()
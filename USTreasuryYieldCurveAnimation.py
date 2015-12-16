
# coding: utf-8

# In[ ]:

'''This program produces an mp4-format video of daily US Treasury yield curves for the US.'''
import matplotlib
matplotlib.use("Agg")
from fredpy import series
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time

# Approximately when the program started
startTime = time.time()


# In[ ]:

# start date, end date, and name for the .mp4 and .ogv files
startDate = '2010-01-01'
endDate = '2500-01-01'
fileName = 'USTreasuryYieldCurveAnimation10Present'


# In[ ]:

# Create Fred objects
y1m= series('DTB4WK')
y3m= series('DTB3')
y6m= series('DTB6')
y1 = series('DGS1')
y5 = series('DGS5')
y10= series('DGS10')
y20= series('DGS20')
y30= series('DGS30')

win = [startDate,endDate]
for y in [y1m,y3m,y6m,y1,y5,y10,y20,y30]:
    y.window(win)

y1m = pd.DataFrame(y1m.data,index = y1m.datenumbers,columns=['1 mo'])
y3m = pd.DataFrame(y3m.data,index = y3m.datenumbers,columns=['3 mo'])
y6m = pd.DataFrame(y6m.data,index = y6m.datenumbers,columns=['6 mo'])
y1 = pd.DataFrame(y1.data,index = y1.datenumbers,columns=['1 yr'])
y5 = pd.DataFrame(y5.data,index = y5.datenumbers,columns=['5 yr'])
y10 = pd.DataFrame(y10.data,index = y10.datenumbers,columns=['10 yr'])
y20 = pd.DataFrame(y20.data,index = y20.datenumbers,columns=['20 yr'])
y30 = pd.DataFrame(y30.data,index = y30.datenumbers,columns=['30 yr'])

yields = pd.concat([y1m,y3m,y6m,y1,y5,y10,y20,y30],axis=1)
yields = yields.dropna(thresh=1)
N = len(yields.index)
print('Date range: '+yields.index[0].to_datetime().strftime('%b %d, %Y')+' to '+yields.index[-1].to_datetime().strftime('%b %d, %Y'))


# In[ ]:

# Initialize figure
fig = plt.figure(figsize=(16,9))
ax = fig.add_subplot(1, 1, 1)
line, = ax.plot([], [], lw=8)
ax.grid()

ax.set_xlim(0,7)
ax.set_ylim(0,18)

ax.set_xticks(range(8))
ax.set_yticks([2,4,6,8,10,12,14,16,18])

xlabels = ['1m','3m','6m','1y','5y','10y','20y','30y']
ylabels = [2,4,6,8,10,12,14,16,18]

ax.set_xticklabels(xlabels,fontsize=20)
ax.set_yticklabels(ylabels,fontsize=20)

figure_title = 'U.S. Treasury Bond Yield Curve'
figure_xlabel = 'Time to maturity'
figure_ylabel = 'Percent'

plt.text(0.5, 1.03, figure_title,horizontalalignment='center',fontsize=30,transform = ax.transAxes)
plt.text(0.5, -.1, figure_xlabel,horizontalalignment='center',fontsize=25,transform = ax.transAxes)
plt.text(-0.05, .5, figure_ylabel,horizontalalignment='center',fontsize=25,rotation='vertical',transform = ax.transAxes)

ax.text(5.75,.25, 'Created by Brian C Jenkins',fontsize=11, color='black',alpha=0.5)#,
dateText = ax.text(0.975, 16.625, '',fontsize=18,horizontalalignment='right')


# In[ ]:

# Initialization function.
def init_func():
    line.set_data([], [])
    return line,


# In[ ]:

# The animation function.
def animate(i):
    global yields
    x = [0,1,2,3,4,5,6,7]
    y = yields.iloc[i]
    line.set_data(x, y)
    dateText.set_text(yields.index[i].to_datetime().strftime('%b %d, %Y'))
    return line ,dateText


# In[ ]:

# Set up the writer
Writer = animation.writers['ffmpeg']
writer = Writer(fps=25, metadata=dict(artist='Brian C Jenkins'), bitrate=3000)

# Make the animation
anim = animation.FuncAnimation(fig, animate, init_func=init_func,frames=N, interval=20, blit=True)


# In[ ]:

# Save the animation as .mp4
anim.save(fileName+'.mp4', writer = writer)


# In[ ]:

# Convert the .mp4 to .ogv
os.system('ffmpeg -i '+fileName+'.mp4 -acodec libvorbis -ac 2 -ab 128k -ar 44100 -b:v 1800k  '+fileName+'.ogv')


# In[ ]:

# Print runtime
seconds = time.time() - startTime
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print("%dh %02dm %02ds"% (h, m, s))


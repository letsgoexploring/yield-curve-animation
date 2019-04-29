#!/usr/bin/env python
# coding: utf-8

# # US Treasury Yield Curve Animation
# 
# The notebook uses daily US Treasury yield data from FRED (https://fred.stlouisfed.org/) to construct an animated visualization of the US Treasury yield curve from January 1965 through the present. Data are downloaded using the `fredpy` module (https://github.com/letsgoexploring/fredpy-package).
# 
# ## Preliminaries

# In[1]:


import matplotlib
matplotlib.use("Agg")
import fredpy as fp
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('classic')
import matplotlib.animation as animation
import os
import time


# In[2]:


# Approximately when the program started
start_time = time.time()


# In[3]:


# start and end dates
start_date = '1965-01-01'
end_date = '2100-01-01'
file_name = '../video/US_Treasury_Yield_Curve_Animation'


# ## Download Data and Merge into `DataFrame`

# In[4]:


# Download data into Fred objects
y1m= fp.series('DTB4WK')
y3m= fp.series('DTB3')
y6m= fp.series('DTB6')
y1 = fp.series('DGS1')
y5 = fp.series('DGS5')
y10= fp.series('DGS10')
y20= fp.series('DGS20')
y30= fp.series('DGS30')

# Give the series names
y1m.data.name = '1 mo'
y3m.data.name = '3 mo'
y6m.data.name = '6 mo'
y1.data.name = '1 yr'
y5.data.name = '5 yr'
y10.data.name = '10 yr'
y20.data.name = '20 yr'
y30.data.name = '30 yr'


# In[5]:


yields = pd.concat([y1m.data,y3m.data,y6m.data,y1.data,y5.data,y10.data,y20.data,y30.data],axis=1)
yields = yields.loc[start_date:end_date]
yields = yields.dropna(thresh=1)
N = len(yields.index)
print('Date range: '+yields.index[0].strftime('%b %d, %Y')+' to '+yields.index[-1].strftime('%b %d, %Y'))


# ## Construct Figure

# In[6]:


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


# ## Create Animation and Save
# 
# Note ffmpeg (https://ffmpeg.org/) is required to save the animation as an mp4 or ogv file.

# In[7]:


# Initialization function
def init_func():
    line.set_data([], [])
    return line,


# In[8]:


# The animation function
def animate(i):
    global yields
    x = [0,1,2,3,4,5,6,7]
    y = yields.iloc[i]
    line.set_data(x, y)
    dateText.set_text(yields.index[i].strftime('%b %d, %Y'))
    return line ,dateText


# In[9]:


# Set up the writer
Writer = animation.writers['ffmpeg']
writer = Writer(fps=25, metadata=dict(artist='Brian C Jenkins'), bitrate=3000)

# Make the animation
anim = animation.FuncAnimation(fig, animate, init_func=init_func,frames=N, interval=20, blit=True)


# In[10]:

# Create a directory called 'Video' in the parent directory if it doesn't exist
try:
    os.mkdir('../Video')
except:
    pass

# Save the animation as .mp4
anim.save(file_name+'.mp4', writer = writer)


# In[11]:


# Convert the .mp4 to .ogv
# os.system('ffmpeg -i '+file_name+'.mp4 -acodec libvorbis -ac 2 -ab 128k -ar 44100 -b:v 1800k  '+file_name+'.ogv')


# ## Print Time to Run

# In[12]:


# Print runtime
seconds = time.time() - start_time
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print("%dh %02dm %02ds"% (h, m, s))


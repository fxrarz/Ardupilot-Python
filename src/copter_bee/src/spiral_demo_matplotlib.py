from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from numpy import *

fig = plt.figure()
ax = plt.axes(projection='3d')
r = linspace(0,10,20)
t = linspace(0,1000,20)
x = r*cos(radians(t))
y = r*sin(radians(t))
z = linspace(0, 20, 20)
ax.plot3D(x, y, z, 'red')
plt.show()

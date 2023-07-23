from numpy import *

r = linspace(0,10,20)
t = linspace(0,1000,20)
x = r*cos(radians(t))
x = (x/10000) - 35.36327092
y = r*sin(radians(t))
y = (y/10000) + 149.16504539
z = linspace(2, 50, 20)
	
f = open("wp.txt", "w")
f.write("QGC WPL 110\n")
f.write("0 1 3 16 0.000000 0.000000 0.000000 0.000000 {} {} {} 1\n".format(-35.36327092, 149.16504539, 1))

for i in range(len(z)):
	f.write("0 0 3 16 0.000000 0.000000 0.000000 0.000000 {} {} {} 1\n".format(x[i].round(8), y[i].round(8), z[i].round(8)))
f.close()

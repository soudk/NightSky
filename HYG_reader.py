import numpy as np 
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import pandas as pd

def sizesBall(minim_mag):
    s = [None]*len(minim_mag)
    for i in range(len(minim_mag)): 
        if 0.0 <= minim_mag[i] and minim_mag[i] <=0.05: 
            s[i] = 50
        elif 0.05 < minim_mag[i] and minim_mag[i] <= 0.1:
            s[i] = 10
        elif 0.1 < minim_mag[i] and minim_mag[i] <= 0.15:
            s[i] = 0.05
        elif 0.15 < minim_mag[i] and minim_mag[i] <= 0.2:
            s[i] = .1
        elif 0.2 < minim_mag[i] and minim_mag[i] <=0.25:
            s[i] = 0.05
        elif 0.25 < minim_mag[i] and minim_mag[i] <= 0.3:
            s[i] = .001
        elif 0.3 < minim_mag[i] and minim_mag[i] <= 0.4:
            s[i] = .00001
        elif 0.4 < minim_mag[i] and minim_mag[i] <= 0.5:
            s[i] = .0000001
    return s



Betelgeuse = SkyCoord('05h55m10.30536s +07d24m25.4304s')
Belt = SkyCoord('05h36m12.8s -01d12m07.00s')
Rigel = SkyCoord('05h14m32.3s -08d12m06.00s')

#data = np.loadtxt('stellar_data.csv',delimiter=',')
data2 = pd.read_csv('hygfull.csv',usecols=['RA','Dec','Mag'])
ra = np.asarray(data2['RA'])
dec = np.asarray(data2['Dec'])
mag = np.asarray(data2['Mag'])


#sizes = sizesBall(mag)

#print (sizes)
plt.scatter((ra/24)*360,dec,marker='*',alpha=0.3)

plt.scatter(88.79,7.40,c='red',marker='*',alpha=0.3)
plt.scatter(84.04,-1.20,c='red',marker='*',alpha=0.3)
plt.scatter(78.63,-8.20,c='red',marker='*',alpha=0.3)


plt.show()
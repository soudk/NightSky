import numpy as np 
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import pandas as pd
from sklearn import preprocessing

class Star:
    def __init__(self, ra, dec, mag,):
        self.position = ra, dec
        self.mag = mag

class Tile:
    def __init__(self, ra_bounds, dec_bounds):
        self.bounds = ra_bounds, dec_bounds


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
df = pd.read_csv('hygfull.csv',usecols=['RA','Dec','Mag'])



#sizes = sizesBall(mag)
df = df[df.Mag <= 6.5] #Only stars visible by naked eye
#print (sizes)
ra = np.asarray(df['RA'])
dec = np.asarray(df['Dec'])
Mag = np.asarray(df['Mag'])

Mag=np.abs(Mag)/max(Mag)
print(max(Mag))

#x = df.Mag #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#Mag_norm = min_max_scaler.fit_transform(x)

#print(x)
ra = np.asarray(df['RA'])
ra = (ra/24)*360 #to degrees
dec = np.asarray(df['Dec'])
plt.scatter(ra,dec,marker='*',alpha=0.7)

#plt.scatter(88.79,7.40,c='red',marker='*',alpha=0.3)
#plt.scatter(84.04,-1.20,c='red',marker='*',alpha=0.3)
#plt.scatter(78.63,-8.20,c='red',marker='*',alpha=0.3)
#plt.show()

tileDec=np.linspace(-90, 90, 36)
tileRA=np.linspace(0, 360, 72)
print(ra)
print(dec)




tiles=[]

for i,val in enumerate(tileRA):
    for j, val2 in enumerate(tileDec):
        if (ra[i] > tileRA[i] and ra[i+1] < tileRA[i+1]) and (dec[j] > tileDec[j] and dec[i+1] < tileDec[i+1]):
            tiles[i].append(ra[i], dec[i], mag[i])

#plt.plot(tiles[2][0], tiles[2][1])
print(tiles)
#plt.show()
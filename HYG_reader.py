import numpy as np 
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import pandas as pd
from sklearn import preprocessing
import scipy.misc


class Star:
    def __init__(self, ra, dec, mag):
        self.position = ra, dec
        self.mag = mag

    def InTile(self,Tiles):
        for t in Tiles:
            if (t.ra_bounds[0] <= self.position[0] <= t.ra_bounds[1]) and (t.dec_bounds[0] <= self.position[1] <= t.dec_bounds[1]):
                t.AddStar(self)

class Tile:
    def __init__(self, ra_bounds, dec_bounds, index,resolution):
        self.ra_bounds = ra_bounds
        self.dec_bounds= dec_bounds
        self.stars=[]
        self.index = index
        self.resolution = resolution

    def AddStar(self, Star):
        self.stars.append(Star)

def init():
    tileDec=np.linspace(-90, 90, 36+1)
    tileRA=np.linspace(0, 360, 72+1)

    #Intializing tiles 
    tiles = []
    for i in range(36*72):
        c = i%(36)
        r = int(i/(36)) 
        tiles.append(Tile((tileRA[r],tileRA[r+1]),(tileDec[c],tileDec[c+1]),i,28))
    
    Stars = []

    for i in range(len(ra)):
        Stars.append(Star(ra[i],dec[i],Mag[i]))
        Stars[i].InTile(tiles)
    
    return Stars,tiles


def blur(tile):
    """
    Function that blurs out the point source depending on the magnitude and size
    """
    pixels = np.zeros([tile.resolution,tile.resolution])
    stars = tile.stars
    ra = tile.ra_bounds
    dec = tile.dec_bounds
    for s in stars: 
        ra_diff = ra[0]-s.position[0]
        dec_diff =  dec[0] - s.position[1] 
        pixels[int(ra_diff)][int(dec_diff)] = s.mag
    return pixels

#def magnitude
#Function that calculates the size of the marker to plot based on magnitude
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
ra = (ra/24)*360 #to degrees


#for i,m in enumerate(Mag):
#    Mag[i] = 1.0 - ((m+abs(min(Mag)))/(max(Mag)+abs(min(Mag))))

#Mag=np.abs(Mag)/max(Mag)
#print(min(Mag), max(Mag))

Stars, tiles = init()

for i,tile in enumerate(tiles):
    pizels = blur(tile)
    scipy.misc.toimage(pizels, cmin=0.0, cmax=1.0).save('tiles/tile'+str(i)+'.jpg')






#x = df.Mag #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#Mag_norm = min_max_scaler.fit_transform(x)

#print(x)
#plt.scatter(ra,dec,marker='*',alpha=0.7)

#plt.scatter(88.79,7.40,c='red',marker='*',alpha=0.3)
#plt.scatter(84.04,-1.20,c='red',marker='*',alpha=0.3)
#plt.scatter(78.63,-8.20,c='red',marker='*',alpha=0.3)
#plt.show()



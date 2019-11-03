import numpy as np 
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import pandas as pd
from sklearn import preprocessing
import scipy.misc

#Gridlines to specify how we split the night sky 
WIDTH_SKY = 12
HEIGHT_SKY = 12

#The resolution of each tile
RESOLUTION_PER_TILE = 118

#To generate training data, we take each tile and shift it 
OVERLAP = 0.1

class Star:
    """
    Create a star object. Each object has a position of right-ascension and declination, and magnitude upon creation
    """
    def __init__(self, ra, dec, mag):
        self.position = ra, dec
        self.mag = mag

    def InTile(self,Tiles):
        """
        Function that bins each star into a tile based on its location
        """
        for t in Tiles:
            if (t.ra_bounds[0] <= self.position[0] <= t.ra_bounds[1]) and (t.dec_bounds[0] <= self.position[1] <= t.dec_bounds[1]):
                t.AddStar(self)

class Tile:
    """
    Creates a tile object, with specified right ascension bounds and declination bounds. 
    """
    def __init__(self, ra_bounds, dec_bounds, index,resolution,shift,shift_type):
        self.ra_bounds = ra_bounds
        self.dec_bounds= dec_bounds
        self.stars=[]
        self.index = index
        self.resolution = resolution
        self.shift = shift
        self.shift_type = shift_type

    def AddStar(self, Star):
        self.stars.append(Star)

def init():
    tileDec=np.linspace(0, 180, WIDTH_SKY+1)
    tileRA=np.linspace(0, 360, HEIGHT_SKY+1)

    #Intializing tiles 
    tiles = []
    for i in range(WIDTH_SKY*HEIGHT_SKY):
        c = i%(WIDTH_SKY)
        r = int(i/(WIDTH_SKY)) 
        tiles.append(Tile((tileRA[c],tileRA[c+1]),(tileDec[r]-90,tileDec[r+1]-90),i,RESOLUTION_PER_TILE,0,None))
        factor = 0.1
        while (factor<=0.9):
            amount_shifted_RA = factor*np.abs((tileRA[c+1]-tileRA[c]))
            amount_shifted_DEC = factor*np.abs((tileDec[r+1]-tileDec[r]))
            
            tiles.append(Tile(((tileRA[c]+amount_shifted_RA)%(360),(tileRA[c+1]+amount_shifted_RA)%(360)),(tileDec[r]-90,tileDec[r+1]-90),i,RESOLUTION_PER_TILE,int(np.round(factor/0.1)),'RA'))
            if r != HEIGHT_SKY-1:
                tiles.append(Tile((tileRA[c],tileRA[c+1]),(tileDec[r]+amount_shifted_DEC-90,tileDec[r+1]+amount_shifted_DEC-90),i,RESOLUTION_PER_TILE,int(np.round(factor/0.1)),'DEC'))
            factor += 0.1

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
    diff_ra = np.abs(ra[1]-ra[0])
    dec = tile.dec_bounds
    diff_dec = np.abs(dec[1]-dec[0])
    for s in stars: 
        if tile.ra_bounds[0]>tile.ra_bounds[1]:
            if s.position[0] > 0 and s.position[0] < 360/WIDTH_SKY:
                ra_diff = ((s.position[0]+(360-ra[0]))/(diff_ra))*RESOLUTION_PER_TILE 
            else: 
                ra_diff = ((s.position[0]-ra[0])/diff_ra)*RESOLUTION_PER_TILE
        else:
            ra_diff = ((s.position[0]-ra[0])/diff_ra)*RESOLUTION_PER_TILE
        dec_diff =  ((dec[1] - s.position[1])/diff_dec)*RESOLUTION_PER_TILE
        pixels[int(np.round(dec_diff%(RESOLUTION_PER_TILE-1)))][int(np.round(ra_diff%(RESOLUTION_PER_TILE-1)))] = s.mag
    return pixels


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
print (len(tiles))

for tile in tiles:
    pizels = blur(tile)
    if tile.shift_type is not None:
        scipy.misc.toimage(pizels, cmin=0.0, cmax=1.0).save('tiles/tile_'+str(tile.index)+'_'+tile.shift_type+str(tile.shift)+'.jpg')
    else: 
        scipy.misc.toimage(pizels, cmin=0.0, cmax=1.0).save('tiles/tile_'+str(tile.index)+'_'+str(tile.shift)+'.jpg')






#x = df.Mag #returns a numpy array
#min_max_scaler = preprocessing.MinMaxScaler()
#Mag_norm = min_max_scaler.fit_transform(x)
tileDec=np.linspace(-90, 90, WIDTH_SKY+1)
tileRA=np.linspace(0, 360, HEIGHT_SKY+1)
#print(x)
plt.scatter(ra,dec,marker='*',alpha=0.7)
for i in tileDec:
    plt.axhline(i)
for j in tileRA:
    plt.axvline(j)
plt.show()
#plt.scatter(88.79,7.40,c='red',marker='*',alpha=0.3)
#plt.scatter(84.04,-1.20,c='red',marker='*',alpha=0.3)
#plt.scatter(78.63,-8.20,c='red',marker='*',alpha=0.3)
#plt.show()



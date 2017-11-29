import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap

class MapDrawer:
    def __init__(self, title):
        self.m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
                    projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
        self.shp_info = m.readshapefile('st99_d00','states',drawbounds=True)
        self.colors = ['r', 'b', 'g', 'c', 'k', 'm', 'y']
        self.color_i = 0
        plt.title('Science & Analytics of Speech')
       
    def add_points(self, lats, lons):
        lons, lats = self.m(lons, lats)
        self.m.scatter(lons, lats, marker='o', color='r', zorder=5)
        self.color_i = self.color_i + 1

    def draw(self):
        plt.show()

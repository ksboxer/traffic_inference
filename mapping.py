from gmplot import GoogleMapPlotter as gmp

'''
key=AIzaSyAe6cOsGe7eb9SuJCOuSxfSdx7LrX8w1l4
'''

def plot_blank_map():
	gmap = gmp.from_geocode("New York City")
	gmap.draw("my_map_example.html")

def plot_from_tbl(tbl):
	gmap = gmp.from_geocode("New York City")
	gmap.scatter(tbl['latitude'], tbl['longitude'], '#3B0B39', size=10, marker=False)
	#gmap.plot(list(tbl['latitude']), tbl['longitude'], 'cornflowerblue', edge_width=10)
	gmap.draw("my_map_example.html")


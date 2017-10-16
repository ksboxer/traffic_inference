
from gmplot import GoogleMapPlotter as gmp


key='key=AIzaSyAe6cOsGe7eb9SuJCOuSxfSdx7LrX8w1l4&'


def plot_blank_map():
	gmap = gmp.from_geocode("New York City")
	gmap.draw("my_map_example.html")

def add_key(file_name):
	with open(file_name, 'r') as myfile:
		website=myfile.read()

	idx_stop = website.index("/api/js?")
	idx_start = website.index("libraries=visualization")
	website_modified = '{}/api/js?{}{}'.format(website[:idx_stop], key, website[idx_start:])
	with open(file_name, "w") as text_file:
		text_file.write(website_modified)




def plot_from_tbl(tbl, configs, bus_route,next_stop):
	gmap = gmp.from_geocode("New York City")
	gmap.scatter(tbl['latitude'], tbl['longitude'], '#3B0B39', size=10, marker=False)
	#gmap.plot(list(tbl['latitude']), tbl['longitude'], 'cornflowerblue', edge_width=10)
	map_file_name = "mapping_htmls/map#{}#{}#{}.html".format(bus_route, next_stop, configs["fake_today"])
	gmap.draw(map_file_name)
	add_key(map_file_name)

def plot_from_tbl_quick(tbl, name):
	gmap = gmp.from_geocode("New York City")
	gmap.scatter(tbl['latitude'], tbl['longitude'], '#3B0B39', size=10, marker=False)
	#gmap.plot(list(tbl['latitude']), tbl['longitude'], 'cornflowerblue', edge_width=10)
	map_file_name = "mapping_htmls/map#{}.html".format(name)
	gmap.draw(map_file_name)
	add_key(map_file_name)


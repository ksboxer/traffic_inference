from gmplot import GoogleMapPlotter as gmp
from bs4 import BeautifulSoup

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




def plot_from_tbl(tbl, configs, bus_route,next_stop, folder):
	gmap = gmp.from_geocode("New York City")
	gmap.scatter(tbl['latitude'], tbl['longitude'], '#3B0B39', size=5, marker=False)
	#gmap.plot(list(tbl['latitude']), tbl['longitude'], 'cornflowerblue', edge_width=10)
	map_file_name = "{}/map#{}#{}#{}.html".format(folder,bus_route, next_stop, configs["fake_today"])
	gmap.draw(map_file_name)
	add_key(map_file_name)

def implant_image(html_file, img_file=None):
	link_doc ='<link rel="stylesheet" type="text/css" href="simple-grid.css"/>'
	link = BeautifulSoup(link_doc)
	soup = BeautifulSoup(open(html_file))
	head = soup.head
	head.insert(0,link)

	grid = """
	  <div class="container">
      <div class="row">
        <div class="col-8">
          <div id="map_canvas" style="width: 100%; height: 100%;"></div>
        </div>
        <div class="col-4">
          <img src="{}">
        </div>
      </div>
    </div>
	""".format(img_file)
	grid_bs = BeautifulSoup(grid)
	soup.find('div',{"id": "map_canvas"}).decompose()
	body = soup.body
	body.append(grid_bs)
	#print(soup)
	with open(html_file, "w") as file:
		file.write(str(soup))



def plot_from_tbl_segments(tbl, previous_stop, stop, folder):
	gmap = gmp(list(tbl['latitude'])[0], list(tbl['longitude'])[0], 16)
	gmap.scatter(tbl['latitude'], tbl['longitude'], '#3B0B39', size=10, marker=False)
	#gmap.plot(list(tbl['latitude']), tbl['longitude'], 'cornflowerblue', edge_width=10)
	map_file_name = "{}/map#{}#{}.html".format(folder,previous_stop, stop)
	gmap.draw(map_file_name)
	add_key(map_file_name)
	implant_image(map_file_name,'/traffic_graph/graph%23{}%23{}.png'.format(previous_stop, stop))



import xmltodict
import json

def get_image_locations(jsonfile):
	# get krystal images spritesheet coordinates
	list = []
	with open(jsonfile, 'r') as f:
		j = json.load(f)
		for i in range(len(j['frames'])):
			x = j['frames'][i]['frame']['x']
			y = j['frames'][i]['frame']['y']
			w = j['frames'][i]['frame']['w']
			h = j['frames'][i]['frame']['h']
			list.append((x, y, w, h))
	return list


def get_krystal_offsets():
	# get krystal images spritesheet coordinates
	list = []
	with open('assets/krystal_images/image_locations.json', 'r') as f:
		j = json.load(f)
		for i in range(len(j['frames'])):
			x_off = j['frames'][i]['offset']['x_off']
			y_off = j['frames'][i]['offset']['y_off']
			list.append((x_off))
	return list


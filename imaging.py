import xmltodict
import json

def get_krystal_locations():
	# get krystal images spritesheet coordinates
	list = []
	with open('krystal_images/image_locations.json', 'r') as f:
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
	with open('krystal_images/image_locations.json', 'r') as f:
		j = json.load(f)
		for i in range(len(j['frames'])):
			x_off = j['frames'][i]['offset']['x_off']
			y_off = j['frames'][i]['offset']['y_off']
			list.append((x_off))
	return list


class Xmlenemies():
	def get_small_dict(self):
		with open('spritesheet_enemies.xml') as fd:
			doc = xmltodict.parse(fd.read())

		spritekeys = {}
		for i in range(57):
			file = doc['TextureAtlas']['SubTexture'][i]['@name'][:-4]
			x = int(doc['TextureAtlas']['SubTexture'][i]['@x'])
			y = int(doc['TextureAtlas']['SubTexture'][i]['@y'])
			width = int(doc['TextureAtlas']['SubTexture'][i]['@width'])
			height = int(doc['TextureAtlas']['SubTexture'][i]['@height'])
			spritekeys[file] = (x/2, y/2, width/2, height/2)
		return spritekeys


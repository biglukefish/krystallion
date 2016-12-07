import xmltodict

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


# Each item in outer list represents a different level.
level_data = [{'bg_image':'assets/level_1_assets/Level_01_Tile_Map_Shorter_Taller.bmp',
			   'bg_tunes':'assets/Retro Reggae.ogg',
			   'tmx_file':'assets/level_1_assets/Level_01_Tile_Map_Shorter_Taller.tmx',
			   'bee_coords':[ (1344, 192), (1920, 256), (3136, 448),
				  (3840, 320), (5504, 448), (6016, 512) ],
			   'vulture_coords': [ (1344, 192), (1920, 256), (3136, 448),
				  (3840, 320), (5504, 448), (6016, 512) ],
			   'shroom_coords': [ (21*64, 9*64, 21*64, 26*64), (8*64, 9*64, 1*64, 9*64) ],
			   'bee_triggers':[ 'self.rect.x > 300', 'self.rect.x > 900',
								'self.rect.x > 2000', 'self.rect.x > 2500',
								'self.rect.x > 4000', 'self.rect.x > 5000' ],
			   'vulture_triggers':[ 'self.rect.x > 300', 'self.rect.x > 900',
									'self.rect.x > 2000', 'self.rect.x > 2500',
									'self.rect.x > 4000', 'self.rect.x > 5000' ]

			   }]
import binascii

level_addresses = [0x11A50, 0x11BE0, 0x11D70, 0x11F00, 0x12090, 0x12220, 0x123B0, 0x12540, 0x126D0]
map_file = '../static/js/maps/map_data.js'

map_data = []
with open('PGOTMO.nes', 'r+b') as f:
	chunk_size = 16*25 # 20 x 20 levels
	for address in level_addresses:
		f.seek(address)
		data = binascii.b2a_hex(f.read(chunk_size), ',')
		map_data.append(data.decode().split(','))

with open(map_file, 'w') as f:
	for i, map_ in enumerate(map_data):
		f.write(f'var level_{i} = [\n')
		for j in range(20):
			row = 19 - j # wizardry has 0,0 in bottom left instead of top left
			f.write('[')
			for col in range(20):
				f.write(f'"{map_[row*20+col]}"')
				if col < 19:
					f.write(',')
			f.write(']')
			if j < 19:
				f.write(',')
			f.write('\n')
		f.write('];\n')

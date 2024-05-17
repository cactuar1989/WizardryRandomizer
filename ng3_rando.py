import binascii
import random


def randomize_ng3(
	rom,
	normal_game,
	skin,
	clothes,
	outline,
	starting_health,
	starting_lives,
	starting_continues,
	windmill,
    fire_wheel,
    dragon_balls,
    vacuum,
    invincible,
	drop_shuffle,
	enemy_shuffle,
	level_shuffle,
	boss_shuffle,
	debug_mode,
	skip_cutscenes,
	seed):
	# print(locals().items())

	def setup_game(f, skin, clothes, outline, hlth, lives, cont, windmill, fire_wheel, 
		dragon_balls, vacuum, invincible, debug, cutscene_skip):
		# default skin is 35
		f.seek(0x7FB1)
		f.write(binascii.unhexlify(skin))
		# default clothes is 22
		f.seek(0x7F61)
		f.write(binascii.unhexlify(clothes))
		# default outline is 07
		f.seek(0x7F11)
		f.write(binascii.unhexlify(outline))
		# max hlth 127 or 0x7F
		f.seek(0x1CC30)
		val = f'{hlth:0>2X}'
		f.write(binascii.unhexlify(val))
		# max lives 127 or 0x7F
		f.seek(0x1CC16)
		val = f'{lives:0>2X}'
		f.write(binascii.unhexlify(val))
		f.seek(0xAA52)
		val = f'{cont:0>2X}'
		f.write(binascii.unhexlify(val))
		# item costs, 5 sequestial bytes
		# f.seek(0x9FDA)
		# costs = f'{windmill:0>2X}{fire_wheel:0>2X}{dragon_balls:0>2X}{vacuum:0>2X}{invincible:0>2X}'
		# f.write(binascii.unhexlify(costs))
		# f.write(binascii.unhexlify(costs))
		# debug bit
		f.seek(0x20009)
		if debug == 'True':
			# default is 70
			if cutscene_skip == 'True':
				f.write(binascii.unhexlify('3F'))
				print('fix cutscene_skip and debug combined')
			else:
				f.write(binascii.unhexlify('3F'))
		else:
			if cutscene_skip == 'True':
				f.write(binascii.unhexlify('F0'))

	def shuffle_drops(f):
		drop_addresses = [
			0xC9FA,0xC9FB,0xC9FC,0xC9FD,0xC9FE,0xC9FF,0xCA00,0xCA01,0xCA02,0xCA07,0xCA08,0xCA09,0xCA0A,0xCA0E,0xCA0F,0xCA10,
			0xCA17,0xCA18,0xCA19,0xCA1A,0xCA1B,0xCA1F,0xCA20,0xCA21,0xCA26,0xCA27,0xCA28,0xCA29,0xCA32,0xCA33,0xCA34,0xCA35,0xCA36,0xCA37,0xCA38,0xCA39,0xCA3C,0xCA3D,
			0xCA46,0xCA47,0xCA48,0xCA49,0xCA4A,0xCA4B,0xCA4C,0xCA52,0xCA53,0xCA54,0xCA55,0xCA56,0xCA67,0xCA68,0xCA69,0xCA9A,0xCA6B,0xCA6C,0xCA73,0xCA74,0xCA75,0xCA76,0xCA77,0xCA78,
			0xCA84,0xCA85,0xCA86,0xCA87,0xCA88,0xCA89,0xCA8A,0xCA8B,0xCA8C,0xCA8D,0xCA95,0xCA96,0xCA97,0xCA98,0xCA99,0xCA9A,0xCA9B,0xCA9F,0xCAA0,0xCAA1,0xCAA8,0xCAA9,0xCAAA,0xCAAB,0xCAAC,
			0xCAC3,0xCAC4,0xCAC5,0xCAC6,0xCAC7,0xCAC8,0xCAC9,0xCAD2,0xCAD3,0xCAD4,0xCAD5,0xCAD6,0xCAD7,0xCAD8,0xCAD9,0xCADC,0xCADD,0xCAE3,0xCAE4,0xCAE5,0xCAE6,0xCAE7,0xCAEC,0xCAED,0xCAEE,0xCAEF,0xCAF3,0xCAF4,0xCAF5,
			0xCAFD,0xCAFE,0xCAFF,0xCB00,0xCB01,0xCB02,0xCB06,0xCB07,0xCB08,0xCB0F,0xCB10,0xCB11,0xCB12,0xCB13,0xCB14,0xCB1A,0xCB1B,0xCB1C,0xCB1D,0xCB1E,0xCB26,0xCB27,0xCB28,0xCB29,0xCB2A,0xCB2B,0xCB2C,
			0xCB37,0xCB38,0xCB39,0xCB3A,0xCB3B,0xCB3C,0xCB3D,0xCB3E,0xCB3F,0xCB44,0xCB45,0xCB46,0xCB47,0xCB4E,0xCB4F,0xCB50,0xCB51,0xCB52,0xCB53,0xCB55,
			0xCB5D,0xCB5E,0xCB5F,0xCB60,0xCB61,0xCB62,0xCB63,0xCB69,0xCB6A,0xCB6B,0xCB6C,0xCB6D,0xCB72,0xCB73,0xCB74,0xCB75,0xCB79,0xCB7A,0xCB7B,0xCB83,0xCB84,0xCB85,0xCB86,0xCB87,0xCB88,0xCB89
			]
		for drop in drop_addresses:
			f.seek(drop)
			value = f.read(1).hex() # return binary byte converted to string
			# turn that string into a list so we can modify one character
			value_str = list(value)
			# # left bit is vertical position, right bit is item type
			# vertical = random.choice(['3','4','5','6','7','8','9','A','B','C'])
			value_str[1] = random.choice(['0','1','2','3','4','5','6','7','8','9','A'])
			value = ''.join(value_str) # back into a string
			f.seek(drop)
			f.write(binascii.unhexlify(value))

	def shuffle_helper(f, start_addr, length, choices):
		f.seek(start_addr)
		for i in range(length):
			enemy_type = random.choice(choices)
			f.write(binascii.unhexlify(enemy_type))

	def shuffle_enemies(f):
		# first val is address, second is number of enemies (number of bytes)
		stage_one_enemies_addr = [(0xCBB5,20),(0xCBE5,14),(0xCC03,8)]
		stage_one_enemies = ['00','01','02','03','04','05','0B','0C','0D','0E','0F','10','12','15','16','17','18','19','1A','1B','1C','1D','1E','1F','20']
		
		stage_two_enemies_addr = [(0xCC3E,18),(0xCC62,6),(0xCC80,12),(0xCCBC,18),(0xCCE4,8)]
		stage_two_enemies = ['00','01','02','03','06','07','08','10','11','12','16','17','18','19','1E','1F']
		
		stage_three_enemies_addr = [(0xCD20,18),(0xCD68,18),(0xCDA9,14),(0xCDE5,14),(0xCE15,14)]
		stage_three_enemies = ['00','01','02','03','04','05','07','08','09','0A','0D','0E','0F','10','12','13','15','1A','1B','1E','1F','20']

		stage_four_enemies_addr = [(0xCE59,18),(0xCE95,18),(0xCEBB,10),(0xCEE4,15)]
		stage_four_enemies = ['00','01','02','03','06','09','0A','10','12','13','18','19','1F','20']
		
		stage_five_enemies_addr = [(0xCF26,24),(0xCF5C,15),(0xCF99,23),(0xCFE0,24),(0xD012,13),(0xD04C,22),(0xD082,16),(0xD0B2,16)]
		stage_five_enemies = ['00','01','02','03','06','0B','0C','0F','10','12','16','17','18','19','1C','1D','1E','1F','20']

		stage_six_enemies_addr = [(0xD0F5,24),(0xD13D,24),(0xD185,24),(0xD1CD,24),(0xD215,24)]
		stage_six_enemies = ['00','01','02','03','04','05','06','07','08','09','0A','0D','0E','0F','10','12','13','16','17','1E','1F','20']

		stage_seven_enemies_addr = [(0xD261,24),(0xD2A9,24),(0xD2F0,23),(0xD319,9),(0xD352,24),(0xD388,15),(0xD3C5,23),(0xD400,18),(0xD430,15)]
		stage_seven_enemies = ['00','01','07','08','09','0A','0D','0E','0F','12','13','14','15','16','17','19','1A','1B','1E','1F','20']
		for addr in stage_one_enemies_addr:
			shuffle_helper(f, addr[0], addr[1], stage_one_enemies)
		for addr in stage_two_enemies_addr:
			shuffle_helper(f, addr[0], addr[1], stage_two_enemies)
		for addr in stage_three_enemies_addr:
			shuffle_helper(f, addr[0], addr[1], stage_three_enemies)
		for addr in stage_four_enemies_addr:
			shuffle_helper(f, addr[0], addr[1], stage_four_enemies)
		for addr in stage_five_enemies_addr:
			shuffle_helper(f, addr[0], addr[1], stage_five_enemies)
		for addr in stage_six_enemies_addr:
			shuffle_helper(f, addr[0], addr[1], stage_six_enemies)
		for addr in stage_seven_enemies_addr:
			shuffle_helper(f, addr[0], addr[1], stage_seven_enemies)

	# def debug_cutscenes(f, debug, cutscene_skip):
	# 	f.seek(0x20009)
	# 	if debug == 'True':
	# 		if cutscene_skip == 'True':
	# 			f.write(binascii.unhexlify('A0'))
	# 		else:
	# 			f.write(binascii.unhexlify('30'))
	# 	else:
	# 		if cutscene_skip == 'True':
	# 			f.write(binascii.unhexlify('F0'))
	def custom_subroutines(f):
		# write level tables
		f.seek(0xB6E0)
		# level list will be shuffled in part or whole to randomize screens/bosses
		levels_list = ['01','02','03','04','05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','19','1A','1B','1C','1D','1E','1F','20','21','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F']
		f.write(binascii.unhexlify('00'))
		f.write(binascii.unhexlify(''.join(levels_list)))
		f.write(binascii.unhexlify('3000')) # always starting at 00 and end at 30
		f.write(binascii.unhexlify(''.join(levels_list)))
		f.write(binascii.unhexlify('30')) # write it twice, second one gets shuffled

		# custom subroutine to grab shuffled screen index and load new level
		f.seek(0xB750)
		level_index_subroutine = 'A6 5F 8A A0 00 D9 00 B7 F0 04 C8 4C 45 B7 BE D0 B6 86 5F A6 5F 18 A5 DC 65 E0 D0 0E 24 6C 70 05 CA A9 40 D0 11 E8 A9 00 F0 0C 24 6C 70 05 E8 A9 00 F0 03 CA A9 40 A8 BD 00 B7 AA 98 86 5F 60'
		f.write(binascii.unhexlify(level_index_subroutine.replace(' ','')))
		# patch existing code to use new subroutine
		f.seek(0xA714)
		level_load_patch = '20 40 B7 EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA EA'
		f.write(binascii.unhexlify(level_load_patch.replace(' ','')))
		# subroutine to fix level shuffle after boss battles
		boss_level_load_sr = 'A9 FF 85 6C 20 40 B7 A2 08 60'
		boss_level_load_patch = '20 90 B7 EA'
		f.seek(0xB7A0)
		f.write(binascii.unhexlify(boss_level_load_sr.replace(' ','')))	
		f.seek(0x1E53D)
		f.write(binascii.unhexlify(boss_level_load_patch.replace(' ','')))


		# # used for shuffling levels or just bosses
		# # subroutine to pick new level codes and put in $5F -> B6D0 (JSR B6C0)
		# # level codes list -> B6D6 for in order, B705 for shuffled
		# # LDY $B6D0,X = BC F6 B6
		# # STY $5F = 84 5F
		# # LDX $5F = A6 5F
		# # RTS = 60
		# f.seek(0xB6D0)
		# f.write(binascii.unhexlify('BC 00 B7 84 5F A6 5F 60'.replace(' ','')))

		# # TXA = 8A
		# # LDY #$00 = A0 00
		# # CMP $B6E6,Y = D9 00 B7 ; if A == B6E6+Y then set zero
		# # BEQ $B763 = F0 04 ; if zero set jump 4 instructions
		# # INY = C8
		# # JMP $B743 = 4C 43 B7 ; if zero clear go backwards
		# # LDX $B715,Y = BE D0 B6 ; put index into X
		# # BVS = 70 05
		# # INX = E8
		# # LDA #$00 = A9 00
		# # BEQ = F0 03
		# # DEX = CA
		# # LDA #$40 = A9 40
		# # TXA = A8
		# # TAY = 8A
		# # LDX $B6F6,Y = BE F6 B6
		# # RTS = 60
		# f.seek(0xB750)
		# f.write(binascii.unhexlify('8A A0 00 D9 00 B7 F0 04 C8 4C 43 B7 BE D0 B6 70 05 E8 A9 00 F0 03 CA A9 40 20 C0 B6 60'.replace(' ','')))
		# # patch rom to use screen number index subroutine
		# f.seek(0xA72D)
		# f.write(binascii.unhexlify('20 40 B7 EA EA EA EA EA EA EA'.replace(' ','')))
		# # patch level incrementing section for cutscenes
		# f.seek(0x1E535)
		# f.write(binascii.unhexlify('20 70 B7 FF FF FF FF FF FF FF'.replace(' ','')))
		# # subroutine to replace it
		# f.seek(0xB780)
		# # A9 00 LDA
		# # 85 E6 STA $E6
		# # A5 5F LDA $5F
		# # 85 E3 STA $E3
		# # E6 5F INC $5F
		# # 60 RTS
		# # f.write(binascii.unhexlify('A5 5F A0 00 D9 00 B7 F0 04 C8 4C 74 B7 BE D0 B6 86 5F A9 00 85 E6 A5 5F 85 E3 E6 5F 60'.replace(' ','')))
		# f.write(binascii.unhexlify('A5 5F A0 00 D9 00 B7 F0 04 C8 4C 74 B7 BE D0 B6 C8 BE 00 B7 86 5F A9 00 85 E6 A5 5F 85 E3 60'.replace(' ','')))

	def shuffle_levels(f):
		levels_list = ['01','02','03','04','05','06','07','08','09','0A','0B','0C','0D','0E','0F','10','11','12','13','14','15','16','17','18','19','1A','1B','1C','1D','1E','1F','20','21','23','24','25','26','27','28','29','2A','2B','2C','2D','2E','2F']
		random.shuffle(levels_list)
		# print(levels_list)
		f.seek(0xB711) # location of shuffled table except 00
		f.write(binascii.unhexlify(''.join(levels_list)))
		f.write(binascii.unhexlify('30')) # always end at 30

	def shuffle_bosses(f):
		if level_shuffle == 'True':
			# if we shuffled the levels the bosses are shuffled too
			return
		boss_screens = ['03','09','0F','14','1D','23','2D','2E','2F']
		table_locations = [0xB713,0xB719,0xB71F,0xB724,0xB72D,0xB733,0xB73C,0xB73D,0xB73E]
		random.shuffle(boss_screens)
		# print(boss_screens)
		for i, addr in enumerate(table_locations):
			f.seek(addr)
			f.write(binascii.unhexlify(boss_screens[i]))
		# set new final boss to trigger ending
		#compare to 2F: 0x1E5A8,0x1E576
		# f.seek(0xA0C1) #8a48, set 8a53,8ab3=screen[7], set 1e486=screen[6]
		# f.write(binascii.unhexlify(boss_screens[8]))


	# main stuff
	with open(rom, 'r+b') as f:
		if normal_game == 'True':
			return rom
		setup_game(f, skin, clothes, outline, starting_health, starting_lives, 
			starting_continues, windmill, fire_wheel, dragon_balls, vacuum,
			invincible, debug_mode, skip_cutscenes)
		# ninpo_cost(f, star, storm, dragon, blades, shield)
		if drop_shuffle == 'True':
			shuffle_drops(f)
		if enemy_shuffle =='True':
			shuffle_enemies(f)
		if level_shuffle == 'True':
			custom_subroutines(f)
			shuffle_levels(f)
		if boss_shuffle == 'True':
			if level_shuffle == 'False':
				custom_subroutines(f)
			shuffle_bosses(f)
	return rom
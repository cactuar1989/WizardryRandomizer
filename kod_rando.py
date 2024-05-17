import binascii
import random
from map_maker import make_map


def randomize_kod(
    rom,
    custom_text,
    easy_spells,
    stair_shuffle,
    key_shuffle,
    curse_shuffle,
    shop_shuffle,
    ep_multiplier,
    monster_shuffle,
    boss_shuffle,
    proc_gen_map,
    seed):

    spoiler = 'Welcome to WIZARDRY RANDO!\nI hope you have fun and let me know if you have suggestions\n'
    spoiler += '=\n'
    spoiler += f'seed={seed}\n'
    spoiler += f'custom_text={custom_text}\n'
    spoiler += f'easy_spells={easy_spells}\n'
    spoiler += f'key_shuffle={key_shuffle}\n'
    spoiler += f'stair_shuffle={stair_shuffle}\n'
    spoiler += f'shop_shuffle={shop_shuffle}\n'
    spoiler += f'curse_shuffle={curse_shuffle}\n'
    spoiler += f'monster_shuffle={monster_shuffle}\n'
    spoiler += f'boss_shuffle={boss_shuffle}\n'
    spoiler += f'ep_multiplier={ep_multiplier}\n'
    spoiler += f'proc_gen_map={proc_gen_map}\n'
    spoiler += 'wizardrycactuar@gmail.com\n'
    spoiler += '=\n'

    maps = ''


    def customize_text(f):
        ouch = [ 'FUCK', 'SHIT', 'CUNT', 'PISS', 'DAMN', 'WOOP', 'ASS!', 'OOF!' ]
        i = random.randint(0, len(ouch)-1)
        ouch = ouch[i].encode('utf-8').hex() # ascii to hex
        f.seek(0x1A669)
        f.write(binascii.unhexlify(ouch))
        # scroll of teleport
        f.seek(0x10507)
        f.write(binascii.unhexlify('91 92 84 95 06 FF 00 00 FF 00 00 00 00 00 15 00 D5 FF 00 00 00 00 00 00 00 00 00 00 00 00 00'.replace(' ',''))) # original value is 85
        f.seek(0x112A3)
        f.write(binascii.unhexlify('4D414C4F52')) # change glass to malor
        # give one to char 1
        f.seek(0x8E9A)
        f.write(binascii.unhexlify('29FFFFFFFF04')) # last byte is inventory count
        msg = "Cactuar's Meadery " # extra space for padding
        f.seek(0x12)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        f.seek(0x74)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        msg = "Avodroc's Inn   "
        f.seek(0x26)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        f.seek(0xB5)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        msg = "Boko's Garage Sale   "
        f.seek(0x38)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        f.seek(0xE5)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        msg = "Char"
        f.seek(0x58)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        f.seek(0x6BB)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        msg = "Poundtown"
        f.seek(0x6B)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        f.seek(0xC8A)
        f.write(binascii.unhexlify(msg.encode('utf-8').hex()))
        msg = "43 61 63 74 75 61 72 27 73 20 57 69 7A 20 49 49 20 52 61 6E 64 6F 22 0B 0A 49 20 68 6F 70 65 20 79 6F 75 22 45 15 68 61 76 65 20 66 75 6E 20 26 20 67 6F 6F 64 20 6C 75 63 6B 21 "
        f.seek(0x88A8)
        f.write(binascii.unhexlify(msg.replace(' ','')))
        msg = "Arby's" # from Castle
        addresses = [0x1BC, 0x2AE8, 0x2C07, 0x32D3, 0x35AE]
        for addr in addresses:
            f.seek(addr)
            f.write(binascii.unhexlify(msg.encode('utf-8').hex()))


    def change_spell_names(f):
        starting_addr = 0x1B9E1
        spell_data = '46 69 72 65 20 20 00 41 43 2D 32 20 20 00 53 6C 65 65 70 20 00 4D 61 70 20 20 20 20 00 44 61 72 6B 20 00 41 43 2D 34 20 00 42 6F 6C 74 20 20 00 46 69 72 65 20 32 20 20 00 42 6F 6C 74 20 32 00 46 65 61 72 20 20 00 48 6F 6C 79 20 20 00 49 63 65 20 20 00 46 69 72 65 20 33 20 20 00 46 65 61 72 20 32 20 20 00 44 65 61 74 68 20 20 20 00 49 63 65 20 32 20 20 00 4B 69 6C 55 6E 64 00 44 65 61 74 68 20 32 20 00 41 43 2D 34 2B 20 20 00 42 6C 65 73 73 00 49 63 65 20 33 20 20 00 57 61 72 70 20 00 42 6C 65 73 73 20 32 00 4D 65 74 65 6F 72 20 20 20 00 5B 42 5D 20 74 6F 20 4C 65 61 76 65 00 41 43 2D 31 20 00 43 75 72 65 00 48 61 72 6D 20 20 00 4C 69 67 68 74 00 41 43 2D 34 20 20 00 41 43 2D 32 00 54 72 61 70 20 00 53 74 6F 6E 65 20 00 53 69 6C 65 6E 63 65 00 46 69 6E 64 20 00 43 75 72 32 00 48 61 72 6D 20 32 00 53 6F 66 74 20 20 00 49 44 20 45 6E 65 6D 79 20 00 4C 69 67 68 74 20 32 00 46 6C 61 72 65 20 20 00 41 43 2D 34 2B 20 00 43 75 72 50 6F 69 73 6F 6E 00 41 43 2D 32 2B 2B 20 20 00 43 75 72 65 20 33 00 48 61 72 6D 20 33 20 20 00 4C 66 00 44 65 74 68 00 48 61 72 6D 34 00 43 75 72 34 00 48 61 72 6D 20 35 00 54 6F 20 43 61 73 74 6C 65 00 48 61 72 6D 20 36 20 00 4C 69 66 65 20 32 20' 
        f.seek(starting_addr)
        f.write(binascii.unhexlify(spell_data.replace(' ','')))


    def shuffle_stairs(f):
        spoiler = ''
        stairs = [
            {'address': 0x8510, 'data': '050502', 'name': 'Stairs to 5E 5N 2D', 'coord': '5E 5N 1D', 'raddr': 0x854C, 'rdata': '050501'},
            {'address': 0x8514, 'data': '100202', 'name': 'Stairs to 16E 2N 2D', 'coord': '16E 2N 1D', 'raddr': 0x8550, 'rdata': '100201'},
            {'address': 0x8554, 'data': '000003', 'name': 'Stairs to 0E 0N 3D', 'coord': '0E 0N 2D', 'raddr': 0x858C, 'rdata': '000002'},
            {'address': 0x855C, 'data': '110203', 'name': 'Stairs to 17E 2N 3D', 'coord': '18E 1N 2D', 'raddr': 0x8590, 'rdata': '120102'},
            {'address': 0x8594, 'data': '0C0C04', 'name': 'Stairs to 12E 12N 4D', 'coord': '12E 12N 3D', 'raddr': 0x85CC, 'rdata': '0C0C03'},
            {'address': 0x859C, 'data': '100204', 'name': 'Stairs to 16E 2N 4D', 'coord': '16E 2N 3D', 'raddr': 0x85D0, 'rdata': '100203'},
            {'address': 0x85D4, 'data': '070C05', 'name': 'Stairs 7E 12N 5D', 'coord': '7E 12N 4D', 'raddr': 0x860C, 'rdata': '070C04'},
            {'address': 0x8610, 'data': '000006', 'name': 'Stairs to 0E 0N 6D', 'coord': '8E 4N 5D', 'raddr': 0x864C, 'rdata': '080405'} ]
        shuffled_stairs = []
        for stair in stairs:
            shuffled_stairs.append({'new_data': stair.get('data'), 'new_name': stair.get('name'), 'new_raddr': stair.get('raddr')})
        random.shuffle(shuffled_stairs)
        for i in range(len(stairs)):
            stairs[i]['new_data'] = shuffled_stairs[i].get('new_data')
            stairs[i]['new_name'] = shuffled_stairs[i].get('new_name')
            stairs[i]['new_raddr'] = shuffled_stairs[i].get('new_raddr')
            f.seek(stairs[i]['address'])
            f.write(binascii.unhexlify(stairs[i]['new_data']))
            f.seek(stairs[i]['new_raddr'])
            f.write(binascii.unhexlify(stairs[i]['rdata']))
            spoiler += f"{stairs[i]['new_name']} at {stairs[i]['coord']}\n"
        spoiler += '=\n'
        return spoiler


    def shuffle_keys(f):
        spoiler = ''
        keys = [ 
            {'address': 0x8520, 'id': '82', 'name': 'Corroded Key', 'coord': '7E 12N 1D'},
            {'address': 0x8560, 'id': '84', 'name': 'Weird Emblem', 'coord': '14E 18N 2D'},
            {'address': 0x8524, 'id': '85', 'name': 'Key of Ebony', 'coord': '17E 6N 1D'},
            {'address': 0x8564, 'id': '86', 'name': 'Key of Cloister', 'coord': '3E 10N 2D'},
            {'address': 0x85A0, 'id': '87', 'name': 'Mithril Key', 'coord': '11E 7N 3D'},
            {'address': 0x85DC, 'id': '88', 'name': 'Master Key', 'coord': '4E 4N 4D'} ]
        key_ids = []
        for key in keys:
            key_ids.append({'new_id': key.get('id'), 'new_name': key.get('name')})
        random.shuffle(key_ids)
        for i in range(len(keys)):
            keys[i]['new_id'] = key_ids[i].get('new_id')
            keys[i]['new_name'] = key_ids[i].get('new_name')
            f.seek(keys[i]['address'])
            f.write(binascii.unhexlify(keys[i]['new_id']))
            spoiler += f"{keys[i]['new_name']} at {keys[i]['coord']}\n"
        return spoiler
     

    def shuffle_shop(f):
        # unequip all items
        # TO DO
        starting_addr = 0x10010
        chunk_size = 31
        item_count = 124 # there are 138 if you want to include the key items in shop
        # put all items into list then shuffle
        f.seek(starting_addr)
        data = binascii.hexlify(f.read(chunk_size * item_count)).decode('utf-8')
        item_list = []
        for index in range(0, len(data), chunk_size * 2):
            item_list.append(data[index : index + chunk_size * 2])
        random.shuffle(item_list)
        f.seek(starting_addr)
        f.write(binascii.unhexlify(''.join(item_list)))


    def shuffle_monsters(f):
        starting_addr = 0xC010
        chunk_size = 11*16 + 4
        f.seek(starting_addr)
        data = binascii.hexlify(f.read(chunk_size)).decode('utf-8') # decode turns the bytes object into a string
        monster_addresses = []
        n = 4
        # split data into 4 byte chunks
        for index in range(0, len(data), n):
            monster_addresses.append(data[index : index + n])
        random.shuffle(monster_addresses)
        f.seek(starting_addr)
        f.write(binascii.unhexlify(''.join(monster_addresses)))


    def shuffle_bosses(f):
        # additional boss of demon lord ID 53 not included
        boss_addresses = [ 0x851C, 0x85B4, 0x85F4, 0x8574, 0x8634, 0x8534 ]
        boss_ids = [ '54 00 83', '55 00 7D', '56 00 7E', '57 00 7F', '58 00 80', '59 00 81' ] # boss id, 00, then item they drop
        random.shuffle(boss_ids)
        index = 0
        for addr in boss_addresses:
            f.seek(addr)
            f.write(binascii.unhexlify(boss_ids[index].replace(' ','')))
            index += 1


    def shuffle_curses(f):
        starting_addr = 0x10016
        chunk_size = 31 # space between each item
        item_count = 138 # kod armor can be cursed too
        for item in range(item_count):
            cursed_data = random.choice(['00','00','00','FF']) # 1/4 chance to be cursed
            f.seek(starting_addr)
            f.write(binascii.unhexlify(cursed_data.replace(' ',''))) # write value without spaces
            starting_addr = starting_addr + chunk_size


    def boost_ep(f, multiplier):
        multiplier = int(multiplier) # comes from html as string which messes up the multiplication, it will concat instead
        starting_addr = 0xC010
        chunk_size = 11*16 + 4
        f.seek(starting_addr)
        data = binascii.hexlify(f.read(chunk_size)).decode('utf-8') # decode turns the bytes object into a string
        monster_addresses = []
        n = 4
        # split data into 4 byte chunks
        for index in range(0, len(data), n):
            monster_addresses.append(data[index : index + n])
        for addr in monster_addresses:
            new_addr = f'{addr[2:]}{addr[:2]}'
            ep_addr = int(new_addr, 16) + 0x4010 + 25
            f.seek(ep_addr)
            ep = int(binascii.hexlify(f.read(4)), 10)
            ep = ep * multiplier
            # pad with zeros to take up 4 bytes space
            ep = str(ep).rjust(8, '0')
            # if we have some overflow just trim it off
            ep = ep[-8:] # only use rightmost 8 chars
            # go back to address, read operation moved our pointer
            f.seek(ep_addr)
            f.write(binascii.unhexlify(ep))


    def shuffle_chars(f):
        starting_addr = 0x8E4D
        chunk_size = 16*6
        names = ['08 43 41 43 54 55 41 52 5F', '08 43 48 41 52 44 43 4F 52', '04 42 4F 4B 4F 20 20 20 20',
            '07 41 56 4F 44 52 4F 43 20', '04 4A 4F 53 48 20 20 20 20', '06 4D 45 47 41 4D 49 20 20',
            '08 56 52 49 41 45 4C 49 53', '04 52 45 53 51 20 20 20 20'] # first byte is name length
        random.shuffle(names)
        for i in range(6):
            f.seek(starting_addr)
            f.write(binascii.unhexlify(names[i].replace(' ','')))
            starting_addr += chunk_size

    def generate_map(f):
        maps = 'KEY\n# = wall\n| = door\nR = room\n\n'
        levels = [0x1201E, 0x124CE, 0x1297E, 0x12E2E, 0x132DE, 0x1378E]
        maze, hex_data = make_map(20, 20, paths=[
            {'start':(0,0), 'end':(5,5)},
            {'start':(5,5), 'end':(7,12)},
            {'start':(7,12), 'end':(14,14)},
            {'start':(14,14), 'end':(19,10)},
            {'start':(0,0), 'end':(10,0)},
            {'start':(10,0), 'end':(17,6)},
            {'start':(10,0), 'end':(15,2)},
            {'start':(15,2), 'end':(16,2)}
            ])
        maps += 'B1F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[0])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(5,5), 'end':(0,0)},
            {'start':(5,5), 'end':(3,10)},
            {'start':(3,10), 'end':(14,18)},
            {'start':(16,2), 'end':(7,1)},
            {'start':(7,1), 'end':(17,1)},
            {'start':(17,1), 'end':(18,2)}
            ])
        maps += 'B2F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[1])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(0,0), 'end':(11,7)},
            {'start':(11,7), 'end':(12,12)},
            {'start':(17,2), 'end':(17,3)},
            {'start':(17,3), 'end':(16,3)},
            {'start':(16,3), 'end':(16,2)}
            ])
        maps += 'B3F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[2])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(12,12), 'end':(7,12)},
            {'start':(7,12), 'end':(3,4)},
            {'start':(6,14), 'end':(7,12)},
            {'start':(17,16), 'end':(12,12)},
            {'start':(16,2), 'end':(16,3)},
            {'start':(3,4), 'end':(4,4)}
            ])
        maps += 'B4F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[3])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(7,12), 'end':(10,4)},
            {'start':(10,4), 'end':(9,4)},
            {'start':(9,4), 'end':(8,4)}
            ])
        maps += 'B5F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[4])
        f.write(binascii.unhexlify(hex_data))
        return maps


    with open(rom, 'r+b') as f:
        shuffle_chars(f)
        if custom_text == 'True':
            customize_text(f)
        if stair_shuffle == 'True':
            spoiler += shuffle_stairs(f)
        if key_shuffle== 'True':
            spoiler += shuffle_keys(f)
        if curse_shuffle == 'True':
            shuffle_curses(f)
        if shop_shuffle == 'True':
            shuffle_shop(f)
        if monster_shuffle == 'True':
            shuffle_monsters(f)
        if boss_shuffle == 'True':
            shuffle_bosses(f)
        if ep_multiplier != '1':
            boost_ep(f, ep_multiplier)
        if easy_spells == 'True':
            change_spell_names(f)
        if proc_gen_map == 'True':
            maps = generate_map(f)
    return rom,spoiler, maps
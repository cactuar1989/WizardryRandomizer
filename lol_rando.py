import binascii
import random
from map_maker import make_map


def randomize_lol(
    rom,
    default_language,
    custom_text,
    easy_spells,
    key_shuffle,
    stair_shuffle,
    shop_shuffle,
    curse_shuffle,
    monster_shuffle,
    boss_shuffle,
    # mortal_lkbreth,
    ep_multiplier,
    proc_gen_map,
    seed):


    spoiler = 'Welcome to WIZARDRY RANDO!\nI hope you have fun and let me know if you have suggestions\n'
    spoiler += '=\n'
    spoiler += f'seed={seed}\n'
    spoiler += f'default_language={default_language}\n'
    spoiler += f'custom_text={custom_text}\n'
    spoiler += f'easy_spells={easy_spells}\n'
    spoiler += f'key_shuffle={key_shuffle}\n'
    spoiler += f'stair_shuffle={stair_shuffle}\n'
    spoiler += f'shop_shuffle={shop_shuffle}\n'
    spoiler += f'curse_shuffle={curse_shuffle}\n'
    spoiler += f'monster_shuffle={monster_shuffle}\n'
    spoiler += f'boss_shuffle={boss_shuffle}\n'
    # spoiler += f'mortal_lkbreth={mortal_lkbreth}\n'
    spoiler += f'ep_multiplier={ep_multiplier}\n'
    spoiler += f'proc_gen_map={proc_gen_map}\n'
    spoiler += 'wizardrycactuar@gmail.com\n'
    spoiler += '=\n'

    maps = ''


    def change_default_lang(f):
        f.seek(0x8540)
        f.write(binascii.unhexlify('0000000000'))


    def change_text(f, addresses, msg):
        for addr in addresses:
            f.seek(addr)
            f.write(binascii.unhexlify(msg.encode('utf-8').hex()))


    def customize_text(f):
        # all addresses of llylgamyn
        change_text(f, [0x6B, 0x5B1, 0x98F, 0x21CF, 0x22A0, 0x404C, 0x4A77, 0x885D, 0x8B31], 'Poundtown')
        change_text(f, [0x12, 0x74], 'Cactuar\'s Meadery ')
        change_text(f, [0x26, 0xC4], 'Avodroc\'s Inn   ')
        change_text(f, [0x58, 0x7E8], 'Char')
        change_text(f, [0x38, 0xF4], 'Boko\'s Garage Sale   ')
        change_text(f, [0x210, 0x1341, 0x23CB, 0x24DE, 0x2B90, 0x3022], 'Castle')
        change_text(f, [0x8869], 'I hope you')
        change_text(f, [0x8876], 'have fun & good luck!')
        # potion of malor
        f.seek(0x10829)
        f.write(binascii.unhexlify('D2')) # originally D6
        change_text(f, [0x10805], 'Malor ')
        f.seek(0x9816)
        f.write(binascii.unhexlify('1D FF FF FF FF 04'.replace(' ',''))) # add to char 1 inventory
        ouch = [ 'FUCK', 'SHIT', 'CUNT', 'PISS', 'DAMN', 'WOOP', 'ASS!', 'OOF!' ]
        i = random.randint(0, len(ouch)-1)
        ouch = ouch[i] # ascii to hex
        # ouch is not stored in one spot so we skip a few addresses per letter
        ouch_addr = 0x1A19C
        chunk_size = 4
        for letter in ouch:
            change_text(f, [ouch_addr], letter)
            ouch_addr += chunk_size


    def change_spell_names(f):
        spell_data = '46 69 72 65 20 20 00 41 43 2D 32 20 20 00 53 6C 65 65 70 20 00 4D 61 70 20 20 20 20 00 44 61 72 6B 20 00 41 43 2D 34 20 00 46 69 72 65 20 32 20 20 00 42 6F 6C 74 20 20 00 46 65 61 72 20 20 00 49 63 65 20 20 00 46 69 72 65 20 33 20 20 00 46 65 61 72 20 32 20 20 00 44 65 61 74 68 20 20 20 00 49 63 65 20 32 20 20 00 44 65 61 74 68 20 32 20 00 4B 69 6C 55 6E 64 00 41 43 2D 34 2B 20 20 00 42 6C 65 73 73 00 57 61 72 70 20 00 42 6C 65 73 73 20 32 00 4D 65 74 65 6F 72 20 20 20'
        f.seek(0x1E10)
        f.write(binascii.unhexlify(spell_data.replace(' ','')))
        spell_data = '41 43 2D 31 2B 00 43 75 72 65 00 48 61 72 6D 20 20 00 4C 69 67 68 74 00 41 43 2D 34 20 20 00 41 43 2D 32 00 54 72 61 70 20 00 53 74 6F 6E 65 20 00 53 69 6C 65 6E 63 65 00 4C 69 67 68 74 20 20 00 43 75 72 65 20 32 00 49 44 20 45 6E 65 6D 79 20 00 41 43 2D 34 2B 20 00 43 75 72 33 00 48 61 72 6D 20 32 00 43 75 72 50 6F 69 73 6F 6E 00 41 43 2D 32 2B 2B 20 20 00 43 75 72 65 20 34 00 48 61 72 6D 20 33 20 20 00 46 6C 61 72 65 20 20 00 46 69 6E 64 20 00 4C 66 00 44 65 74 68 00 48 61 72 6D 34 00 4C 69 66 32 00 48 61 72 6D 20 35 00 54 6F 20 43 61 73 74 6C 65 00 48 6F 6C 79 20 20 20 00 4C 69 66 65 20 32 20'
        f.seek(0x1F10)
        f.write(binascii.unhexlify(spell_data.replace(' ','')))


    def shuffle_stairs(f):
        spoiler = ''
        stairs = [
        {'address': 0x855C, 'data': '070104', 'name': 'Stairs to 7E 1N 4F', 'coord': '7E 7N 1F', 'raddr': 0x8620, 'rdata': '070701'},
        {'address': 0x8560, 'data': '120005', 'name': 'Stairs to 18E 0N 5F', 'coord': '7E 6N 1F', 'raddr': 0x867C, 'rdata': '070601'},
        {'address': 0x8570, 'data': '130002', 'name': 'Stairs to 19E 0N 2F', 'coord': '19E 13N 1F', 'raddr': 0x8590, 'rdata': '130D01'},
        {'address': 0x8574, 'data': '020203', 'name': 'Stairs to 2E 2N 3F', 'coord': '19E 14N 1F', 'raddr': 0x85D0, 'rdata': '130E01'},
        {'address': 0x85A4, 'data': '0A0204', 'name': 'Stairs to 10E 2N 4F', 'coord': '0E 19N 2F', 'raddr': 0x8610, 'rdata': '001302'},
        {'address': 0x85DC, 'data': '0B0005', 'name': 'Stairs to 11E 0N 5F', 'coord': '0E 1N 3F', 'raddr': 0x8678, 'rdata': '000103'},
        {'address': 0x8614, 'data': '050006', 'name': 'Stairs to 5E 0N 6F', 'coord': '19E 14N 4F', 'raddr': 0x8690, 'rdata': '130E04'},
        {'address': 0x8650, 'data': '0E0006', 'name': 'Stairs to 14E 0N 6F', 'coord': '0E 13N 5F', 'raddr': 0x8694, 'rdata': '000D05'}]
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
        print('TO DO: put neutral crystal into key item rotation with logic')
        # 01=orb(6F), 02=n crystal, 03=evil crystal(Delf), 04=good crystal(Angel), 07=amulet of air(Po'le), 
        # 08=holy water(10E 19N 3F), 09=rod of fire(4E 7N 5F), 0A=gold medallion(7E 7N 3F), 0B=bad orb(6F)
        spoiler = ''
        #
        # CHANGING THE ORDER WILL BREAK CODE BELOW!
        #
        keys = [
            {'address': 0xED4E, 'id': '07', 'name': 'Amulet of Air', 'coord': '11E 19N 2F (Po\'le)'},
            {'address': 0x85E2, 'id': '0A', 'name': 'Gold Medallion', 'coord': '7E 7N 3F (Trade broadsword)'},
            {'address': 0x85F2, 'id': '08', 'name': 'Holy Water', 'coord': '10E 19N 3F (Trader)'},
            {'address': 0xED43, 'id': '03', 'name': 'Crystal of Evil', 'coord': '7E 17N 4F (Delf)'},
            {'address': 0xED3B, 'id': '04', 'name': 'Crystal of Good', 'coord': '12E 10N 5F (Angel)'},
            {'address': 0x868A, 'id': '09', 'name': 'Rod of Fire', 'coord': '4E 7N 5F (Temple of Fung)'},
            {'address': 0x86C2, 'id': '01', 'name': 'Orb or Earithin', 'coord': '17E 17N 6F'},
            {'address': 0x86C6, 'id': '0B', 'name': 'Orb of Mhuuzfes', 'coord': '13E 2N 6F'}
            ]
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
        # change Holy Water trade requirement to something we have
        f.seek(0x85F0) # address of item they want from you to get holy water back
        items = [0, 1, 3, 4, 5]
        rec = keys[2]['new_id']
        for item in items:
            # removing the item from list that matches trader's item
            if keys[item]['new_id'] == rec:
                print(f"removing {keys[item]['new_name']}")
                items.remove[item]
        r = random.choice(items) # breaks if we change list order above. could dynamically create list but not worth effort
        f.write(binascii.unhexlify(keys[r]['new_id']))
        spoiler += f"10E 19N 3F Trader={keys[r]['new_name']} for {keys[2]['new_name']}\n"
        # logic to check if we could get both crystals before lkbreth
        e_crystal = False
        g_crystal = False
        for i,key in enumerate(keys[0:6]):
            if keys[i]['new_id'] == '03':
                e_crystal = True
            elif keys[i]['new_id'] == '04':
                g_crystal = True
        # change lkbreth item req to something we will have before 6F (10E 3N 6F)
        f.seek(0x1BA67) # address of hard coded value for his item req
        # we will always be able to get amulet of air, gold medallion, holy water(new id), crystal of good/evil and rod of fire
        items = [0,1,2,3,4,5]
        if e_crystal == True and g_crystal == True:
            items.append('n_crystal')
        r = random.choice(items) # exclude last 2 (6F orbs)
        if r == 'n_crystal':
            spoiler += f"L'kbreth pass item=Neutral Crystal\n"
        elif keys[r]['id'] == '08':
            # we don't want holy water we want whatever it was replaced with
            f.write(binascii.unhexlify(keys[r]['new_id']))
            spoiler += f"L'kbreth pass item={keys[r]['new_name']}\n"
        else:
            f.write(binascii.unhexlify(keys[r]['id']))
            spoiler += f"L'kbreth pass item={keys[r]['name']}\n"
        return spoiler
     


    def shuffle_shop(f):
        starting_addr = 0x104A5 # starting after broadsword for trading logic
        chunk_size = 61
        item_count = 94
        f.seek(starting_addr)
        data = binascii.hexlify(f.read(chunk_size * item_count)).decode('utf-8')
        item_list = []
        for index in range(0, len(data), chunk_size * 2):
            item_list.append(data[index : index + chunk_size * 2])
        random.shuffle(item_list)
        f.seek(starting_addr)
        f.write(binascii.unhexlify(''.join(item_list)))


    def shuffle_curses(f):
        starting_addr = 0x10267
        chunk_size = 61 # space between each item
        item_count = 105 # not including orbs and crystals
        for item in range(item_count):
            cursed_data = random.choice(['00','00','00','FF']) # 1/4 chance to be cursed
            f.seek(starting_addr)
            f.write(binascii.unhexlify(cursed_data.replace(' ',''))) # write value without spaces
            starting_addr = starting_addr + chunk_size


    def shuffle_monsters(f):
        table_start = 0x14010
        starting_addr = table_start
        chunk_size = 2
        num_monsters = 72 # 78 including bosses
        monster_addresses = []
        for i in range(num_monsters):
            f.seek(starting_addr)
            data = binascii.hexlify(f.read(chunk_size)).decode('utf-8') # decode turns the bytes object into a string
            monster_addresses.append(data)
            starting_addr += chunk_size
        random.shuffle(monster_addresses)
        f.seek(table_start)
        f.write(binascii.unhexlify(''.join(monster_addresses)))


    def make_mortal_lkbreth(f):
        print('TO DO: make lkbreth mortal')
        # f.seek(0x159EA)
        # new_ac = '04'
        # f.write(binascii.unhexlify(new_ac))


    def shuffle_bosses(f):
        # 00=moat monster, 01=high corsair, 48=priest of fung, 49=angel, 4A=delf, 4B=delf's minions, 4C=po'le, 4D=l'kbreth
        boss_addresses = [0x85C0, 0x8637, 0x867F, 0x8593]
        boss_ids = ['08 48 FF FF', '24 49 00 49', '22 4A 00 4A', '08 4C FF FF']
        random.shuffle(boss_ids)
        index = 0
        for addr in boss_addresses:
            f.seek(addr)
            f.write(binascii.unhexlify(boss_ids[index].replace(' ','')))
            index += 1


    def boost_ep(f, multiplier):
        multiplier = int(multiplier) # comes from html as string which messes up the multiplication, it will concat instead
        monster_addr = [
            0x140F3, 0x14148, 0x14197, 0x141E6, 0x14235, 0x14284, 0x142D3, 0x14322, 0x14374, 0x143C6,
            0x14418, 0x1446A, 0x144BF, 0x1450E, 0x1455D, 0x145AC, 0x14601, 0x14650, 0x146A2, 0x146F7,
            0x14746, 0x1479B, 0x147F0, 0x14842, 0x14897, 0x148EC, 0x1493E, 0x14990, 0x149E5, 0x14A3A,
            0x14A89, 0x14ADE, 0x14B30, 0x14B82, 0x14BD1, 0x14C20, 0x14C6F, 0x14CC7, 0x14D19, 0x14D6E,
            0x14DC3, 0x14E15, 0x14E6D, 0x14EC5, 0x14F17, 0x14F6C, 0x14FBE, 0x15013, 0x15068, 0x150BD,
            0x15112, 0x15167, 0x151BF, 0x15214, 0x15266, 0x152B5, 0x1530A, 0x1535F, 0x153B1, 0x15406,
            0x15458, 0x154B0, 0x15502, 0x15551, 0x155A6, 0x155F5, 0x1564D, 0x156A5, 0x156F7, 0x15749,
            0x157A1, 0x157F3, 0x15854, 0x158A6, 0x158F8, 0x15950, 0x159A2, 0x159F7
            ]
        # monster data not evenly spaced so i can't iterate with a chunk size. idk where the address table is yet
        for addr in monster_addr:
            f.seek(addr)
            ep = int(binascii.hexlify(f.read(4)), 10)
            ep = ep * multiplier
            # pad with zeros to take up 4 bytes space
            ep = str(ep).rjust(8, '0')
            # if we have some overflow just trim it off
            ep = ep[-8:] # only use rightmost 8 chars
            # go back to address, read operation moved our pointer
            f.seek(addr)
            f.write(binascii.unhexlify(ep))


    def shuffle_chars(f):
        starting_addr = 0x97C9
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
            {'start':(0,0), 'end':(0,10)},
            {'start':(0,10), 'end':(19,15)},
            {'start':(19,15), 'end':(19,14)},
            {'start':(19,14), 'end':(19,13)},
            {'start':(0,0), 'end':(7,7)},
            {'start':(7,7), 'end':(7,6)}
            ])
        maps += '1F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[0])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(0,19), 'end':(19,0)},
            {'start':(0,19), 'end':(11,19)}
            ])
        maps += '2F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[1])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(0,1), 'end':(2,2)},
            {'start':(2,2), 'end':(7,7)},
            {'start':(7,7), 'end':(10,19)}
            ])
        maps += '3F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[2])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(7,1), 'end':(10,2)},
            {'start':(10,2), 'end':(7,17)},
            {'start':(7,17), 'end':(19,14)}
            ])
        maps += '4F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[3])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(0,13), 'end':(4,8)},
            {'start':(4,8), 'end':(4,7)},
            {'start':(11,0), 'end':(18,0)},
            {'start':(18,0), 'end':(12,10)},
            {'start':(12,10), 'end':(0,13)}
            ])
        maps += '5F\n'
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
        if default_language == 'english':
            change_default_lang(f)
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
        # if mortal_lkbreth == 'True':
        #     make_mortal_lkbreth(f)
        if ep_multiplier != '1':
            boost_ep(f, ep_multiplier)
        if easy_spells == 'True':
            change_spell_names(f)
        if proc_gen_map == 'True':
            maps = generate_map(f)
    return rom, spoiler, maps
import binascii
import random
from map_maker import make_map


def randomize_pgotmo(
    rom,
    custom_text,
    easy_spells,
    stair_shuffle, 
    key_shuffle, 
    curse_shuffle, 
    shop_shuffle, 
    buff_coins, 
    disable_elevator, 
    infinite_potions,
    ep_multiplier,
    monster_shuffle,
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
    spoiler += f'buff_coins={buff_coins}\n'
    spoiler += f'monster_shuffle={monster_shuffle}\n'
    spoiler += f'ep_multiplier={ep_multiplier}\n'
    spoiler += f'proc_gen_map={proc_gen_map}\n'
    spoiler += 'wizardrycactuar@gmail.com\n'
    spoiler += '=\n'

    maps = ''


    def change_text(f, addresses, msg):
        for addr in addresses:
            f.seek(addr)
            f.write(binascii.unhexlify(msg.encode('utf-8').hex()))


    def customize_text(f):
        for address in text_changes:
            f.seek(address)
            f.write(binascii.unhexlify(text_changes[address].replace(' ','')))
        change_text(f, [0x576, 0x1AE8, 0x1B8B, 0x118AB], 'COLLAR')
        change_text(f, [0x5BC], '  will allow you to scoop the ') # congrats msg
        change_text(f, [0x5DB], 'royal litter box')
        change_text(f, [0x5F0], 'Then  she  also  scratched  ')
        change_text(f, [0x60D], 'you in the eye... What a grump')
        change_text(f, [0x62C], 'ass. Here\'s an uwu, please go.')
        change_text(f, [0x425], 'Suspicious Box') # trapless chest 14
        change_text(f, [0x43C], 'Cactus Needle') # poison needle 13
        change_text(f, [0x44B], 'Ass Bomb') # gas bomb 8
        change_text(f, [0x455], 'Peanut Butter') # crossbow bolt 13
        change_text(f, [0x464], 'Wet Socks!   ') # exploding box 13
        change_text(f, [0x473], 'Shocker') # stunner 7
        change_text(f, [0x47C], 'Portapotty') # teleporter 10
        change_text(f, [0x488], 'Hangover     ') # mage's misery 13
        change_text(f, [0x4A7], 'AHHHH') # alarm 5
        change_text(f, [0x497, 0x4AE], 'Hot Girl Shit  ') # cleric's crisis 15
        change_text(f, [0x701], 'You fuckin died!') # in rock
        change_text(f, [0x748], 'O SHIT') # a pit!
        change_text(f, [0x76F], 'Pay up mother fucker') # who shall we help?
        change_text(f, [0x3591], 'Pay or they die.') # cheap apostates!
        change_text(f, [0x35A2], 'idc.') # out!


    text_changes = {
        0x1F8C6: 'FD', # AC bug fix (change F9 to FD)
        0xDE7: '20 20 20 2A 2A 2A 20 54 52 41 4E 53 20 52 49 47 48 54 53 20 2A 2A 2A 20 20 20', 
        0x38D: '68 72 65 77 20 70 6F 6F 70 20 61 74', # threw poop at
        # New trap names
        # 0x425: '53 75 73 70 69 63 69 6F 75 73 20 42 6F 78 FF 54 72 61 70 3F FF FF 20 43 61 63 74 75 73 20 4E 65 65 64 6C 65 FF 20 41 73 73 20 42 6F 6D 62 FF 20 50 65 61 6E 75 74 20 42 75 74 74 65 72 FF 20 57 65 74 20 53 6F 63 6B 73 20 20 20 20 FF 20 53 74 75 6E 6E 65 72 FF 20 54 65 6C 65 70 6F 72 74 65 72 FF 20 48 61 6E 67 6F 76 65 72 20 20 20 20',
        0x58C: '43 61 74 20 4C 61 64 79', # Overlord to Cat Lady
        0x5B3: '43 61 74 20 4C 61 64 79', # Overlord to Cat Lady
        0x7C0: '43 61 74 20 4C 61 64 79', # Overlord to Cat Lady
        0x41C4: '43 61 74 20 4C 61 64 79', # Overlord to Cat Lady
        0xB96: '43 61 63 74 75 61 72 27 73 20 4D 65 61 64 65 72 79 20', # Cactuar's meadery
        0xD31: '43 61 63 74 75 61 72 27 73 20 4D 65 61 64 65 72 79 20', # Cactuar's meadery
        0xBDC: '43 68 61 72', # Temple of Char
        0x768: '68 61 72', # Temple of Char
        0x182BB: '54 68 69 73 20 67 61 6D 65 20 66 75 63 6B 73 21 CF 02 20 20 21 E8 10 20 4C 65 74 27 73 20 67 65 74 20 77 65 69 72 64', # This game fucks Let's get weird
        0x182F2: '20 20 20 74 68 65 20 73 68 69 74 20 73 68 6F 77 20 20 20 20 20', # the shit show
        0x994: '76 6F 64 72 6F 63 27 73 20 49 6E 6E 20 20 20', # Avodroc's Inn
        0xBAB: '76 6F 64 72 6F 63 27 73 20 49 6E 6E 20 20 20', # Avodroc's Inn
        0xB8F: '20 49 48 4F 50 20', # Castle to IHOP
        0xBBC: '42 6F 6B 6F 27 73 20 54 72 61 64 69 6E 67 20 50 6F 73 74 20 20', # Boko's Trading post
        0xD88: '42 6F 6B 6F 27 73 20 54 72 61 64 69 6E 67 20 50 6F 73 74 20 20', # Boko's Trading post
        0x010CA4: '54 45 4C 45 50 4F 52 54 20 20 20 20 20 20 05 07 00 FF FF 00 00 00 00 00 25 00 01 12', # Scroll of Teleport in shop
        0x888: '46 75 63 6B', # Ouch to Fuck
        # Replace 0E,0N,10D message with Steiner Math
        0x1CA6: 'FF 22 59 6F 75 20 6B 6E 6F 77 20 74 68 65 79 20 73 61 79 20 61 6C 6C 20 6D 65 6E 20 61 72 65 20 63 72 65 61 74 65 64 20 65 71 75 61 6C 2C 20 62 75 74 20 79 6F 75 20 6C 6F 6F 6B 20 61 74 20 6D 65 20 61 6E 64 20 79 6F 75 20 6C 6F 6F 6B 20 61 74 20 54 72 65 62 6F 72 20 61 6E 64 20 79 6F 75 20 63 61 6E 20 73 65 65 20 74 68 61 74 20 73 74 61 74 65 6D 65 6E 74 20 69 73 20 6E 6F 74 20 74 72 75 65 21 22 FF FF FF FF 50 53 20 2D 20 49 20 47 4F 54 20 31 34 31 20 26 20 32 2F 33 20 43 48 41 4E 43 45 20 4F 46 20 57 49 4E 4E 49 4E FF FF FF FF FF FF FF FF FF FF FF FF 50 50 50 53 20 2D 20 49 20 47 4F 54 20 31 34 31 20 26 20 32 2F 33 20 43 48 41 4E 43 45 20 4F 46 20 57 49 4E 4E 49 4E FF'
    }


    premade_characters = [
        # [available] [name length 0-8] [name*8] [race] [class] [alignment] [str] [iq] [pie] 
        # [vit] [agi] [luck] [gold*6] [ep*6] [current hp hi bit] 
        # [current hp low bit] [max hp*2] [lvl*2] [status] [age]
        # CACTUAR
        '01 08 43 41 43 54 55 41 52 5F 04 03 01 05 07 07 06 10 0F 00 00 00 00 01 52 00 00 00 00 00 00 00 05 00 05 00 01 05 0E 18 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 C3 D4 2E 5A 39 12 08 08 08 08 08 08 08 08 72 29',
        # CHARDCOR
        '01 08 43 48 41 52 44 43 4F 52 01 06 02 08 0B 07 0A 09 15 00 00 00 00 00 00 00 00 00 00 00 00 00 08 00 08 00 01 00 10 18 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 80 00 00 00 00 00 01 08 0B 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 C9 A5 21 08 41 0C 08 08 08 89 1C 0B 08 08 EC CC',
        # BOKO
        '01 04 42 4F 4B 4F 20 20 20 20 00 07 02 0B 09 08 0A 08 08 00 00 00 00 00 00 00 00 00 00 00 00 00 08 00 08 00 01 00 10 18 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 80 00 00 00 00 00 01 08 0B 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 C9 A6 21 08 41 0C 08 08 08 89 1C 0B 08 08 94 EE', 
        # AVODROC
        '01 07 41 56 4F 44 52 4F 43 20 03 04 02 07 0B 0B 09 08 07 00 00 00 00 00 00 00 00 00 00 00 00 00 08 00 08 00 01 00 10 18 04 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 40 00 00 00 00 80 80 80 00 00 00 00 00 03 09 00 00 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 C3 76 21 08 41 0C 09 09 48 89 1E 0B 08 08 1C 60',
        # JOSH 
        '01 04 4A 4F 53 48 20 20 20 20 02 05 02 0B 08 08 09 0A 07 00 00 00 00 00 00 00 00 00 00 00 00 00 08 00 08 00 01 00 10 18 06 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 80 80 80 00 00 00 00 00 02 07 0A 00 00 00 00 00 03 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 B1 65 2B 08 41 0E 08 08 08 89 1B 0B 08 08 E7 1D',
        # MEGAMI 
        '01 06 4D 45 47 41 4D 49 20 20 00 01 02 08 0B 07 08 08 09 00 00 00 00 00 00 00 00 00 00 00 00 00 08 00 08 00 01 00 0E 18 09 01 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00 00 00 00 80 00 00 00 00 00 00 00 09 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7B 63 21 08 3F 12 09 08 0C 88 11 09 08 08 81 62',
        # VRIAELISS 
        '01 08 56 52 49 41 45 4C 49 53 04 01 02 08 0C 09 07 0A 0C 00 00 00 00 00 00 00 00 00 00 00 00 00 08 00 08 00 01 00 0F 18 09 01 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00 00 00 00 80 00 00 00 00 00 00 00 09 2E 00 00 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7A 63 21 08 40 12 09 08 0C 88 11 09 08 08 D8 3C',
        # RESQ 
        '01 04 52 45 53 51 20 20 20 20 04 01 02 08 0C 09 07 0A 0C 00 00 00 00 00 00 00 00 00 00 00 00 00 08 00 08 00 01 00 0F 18 09 01 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 04 00 00 00 00 00 00 80 00 00 00 00 00 00 00 09 2E 00 00 00 00 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 7A 63 21 08 40 12 09 08 0C 88 11 09 08 08 D8 3C' 
    ]


    key_items = {
        'bear_statue': {'address': 0x12D82, 'value': '5F', 'coord': '9E 18N 2D', 'name': 'STATUEofBEAR'},
        'frog_statue': {'address': 0x12D86, 'value': '60', 'coord': '12E 4N 2D', 'name': 'STATUEofFROG'},
        'bronze_key': {'address': 0x12B9E, 'value': '61', 'coord': '13E 3N 1D', 'name': 'KEYofBRONZE'},
        'silver_key': {'address': 0x12BA2, 'value': '62', 'coord': '13E 18N 1D', 'name': 'KEYofSILVER'},
        'gold_key': {'address': 0x12D7E, 'value': '63', 'coord': '4E 16N 2D', 'name': 'KEYofGOLD'},
        'blue_ribbon': {'address': 0x13122, 'value': '64', 'coord': '11E 10N 4D', 'name': 'BLUE RIBBON'}
    }


    stairs = {
        # only included descents for now that way you can backtrack
        '1F_down': {'address': 0x12B89, 'value': '0C 07 02', 'raddr': 0x12D55, 'rvalue': '00 0A 01', 'coord': '0E 10N 1D', 'name': 'Stairs to 2F'}, # 12E  7N 2D when you exit the 1F stairs going down
        '2F_down': {'address': 0x12D61, 'value': '0F 0B 03', 'raddr': 0x12F25, 'rvalue': '10 0F 02', 'coord': '16E 15N 2D', 'name': 'Stairs to 3F'}, # 15E 11N 3D
        '3F_down': {'address': 0x12F29, 'value': '0A 12 04', 'raddr': 0x130F5, 'rvalue': '01 08 03', 'coord': '1E 8N 3D', 'name': 'Stairs to 4F'}, # 10E 18N 4D
        '4F_down': {'address': 0x13129, 'value': '00 00 05', 'raddr': 0x132C5, 'rvalue': '11 07 04', 'coord': '17E 7N 4D', 'name': 'Stairs to 5F'}, #  0E  0N 5D
        '5F_down': {'address': 0x132C9, 'value': '13 13 06', 'raddr': 0x13495, 'rvalue': '08 08 05', 'coord': '8E 8N 5D', 'name': 'Stairs to 6F'}, # 19E 19N 6d
        '6F_down': {'address': 0x13499, 'value': '0A 0A 07', 'raddr': 0x13665, 'rvalue': '08 10 06', 'coord': '8E 16N 6D', 'name': 'Stairs to 7F'}, # 10E 10N 7d
        '7F_down': {'address': 0x13669, 'value': '09 0B 08', 'raddr': 0x13835, 'rvalue': '12 09 07', 'coord': '18E 9N 7D', 'name': 'Stairs to 8F'}  #  9E 11N 8d
    }


    fixed_encounters = [
        0x12B9A # 1F Murphy's Ghost
    ]


    potions = [
        0x104F6, # Potion of Curing
        0x10536, # Potion of Neutralizing
        0x10676 # Sleep
    ]


    def change_spell_names(f):
        starting_addr = 0x3DF5
        chunk_size = 10 # each spell has 10 bytes of name space but last byte must be a space (9 for name itself)
        spell_names = ['Fire', 'AC-2', 'Sleep', 'Location', 'Darkness', 'AC-4', 'Fire 2', 'Bolt',
            'Fear', 'Ice', 'Fire 3', 'Fear 2', 'Death', 'Ice 2', 'Death 2', 'KillUnded',
            'AC-4 All', 'Bless', 'Teleport', 'Bless 2', 'Meteor',
            'AC-1 All', 'Cure', 'Harm', 'Light', 'AC-4', 'AC-2 All', 'ID Trap', 'Paralyze', 'Silence', 'Light 2',
            'Soft', 'ID Enemy', 'AC-4 All', 'Cure 2', 'Harm 2', 'RmvPoison', 'AC-2 All+', 'Cure 3', 'Harm 3',
            'Harm 4', 'Find Body', 'Life', 'Death', 'Harm 5', 'Full Cure', 'Harm 6', 'To Castle', 'Holy', 'Full Life']
        for spell in spell_names:
            f.seek(starting_addr)
            spell = spell.ljust(10, ' ') # pad to 10 chars, left-justified
            h = spell.encode('utf-8').hex() # ascii to hex
            f.write(binascii.unhexlify(h))
            starting_addr += chunk_size


    def make_potions_reusable(f):
        for potion_addr in potions:
            f.seek(potion_addr)
            f.write(binascii.unhexlify('00'))


    def shuffle_shop(f):
        starting_addr = int(0x10130) # address of first item in rom (not including the name)
        num_items = 94 # 101 if you want to include key items
        for i in range(num_items):
            # offset from base
            shop_count = starting_addr + 14
            shop_data = random.choice(['00','00','00','FF','01'])
            # offset to next item
            f.seek(shop_count)
            f.write(binascii.unhexlify(shop_data.replace(' ',''))) # write value without spaces
            starting_addr = starting_addr + 64


    def shuffle_curses(f):
        starting_addr = int(0x10130) # address of first item in rom (not including the name)
        num_items = 94
        for i in range(num_items):
            # offset from base
            cursed = starting_addr + 4
            cursed_data = random.choice(['00','00','00','FF']) # 1/4 chance to be cursed
            f.seek(cursed)
            f.write(binascii.unhexlify(cursed_data.replace(' ',''))) # write value without spaces
            starting_addr = starting_addr + 64



    def shuffle_monsters(f):
        starting_addr = 0x14010
        monsters = []
        chunk_size = 16*8 # bytes per monster
        # read each monster (101 total) into list as strings
        for i in range(101):
            f.seek(starting_addr)
            data = binascii.hexlify(f.read(chunk_size))
            monsters.append(data)
            starting_addr += chunk_size
        random.shuffle(monsters) # shuffle list
        starting_addr = 0x14010 # reset address back to start
        # write entire list back to file
        for i in range(len(monsters)):
            f.seek(starting_addr)
            f.write(binascii.unhexlify(monsters[i]))
            starting_addr += chunk_size


    def shuffle_chars(f):
        starting_addr = 0x17310
        chunk_size = 16*8
        random.shuffle(premade_characters)
        # game only allows 6 premades
        for i in range(6):
            f.seek(starting_addr)
            f.write(binascii.unhexlify(premade_characters[i].replace(' ','')))
            starting_addr += chunk_size


    def disable_elevators(f):
        # Behavior tile addresses for both elevators on each floor
        e_1F_to_4F = [0x12BA4, 0x12D74, 0x12F3C, 0x1310C]
        e_4F_8F = [0x13110, 0x132D4, 0x1349C, 0x1366C, 0x1383C]
        # Replace elevator behavior with message 16
        msg_address = 0x17D5
        msg = '43 6C 6F 73 65 64 20 66 6F 72 20 6D 61 69 6E 74 65 6E 61 6E 63 65'
        f.seek(msg_address)
        f.write(binascii.unhexlify(msg.replace(' ','')))
        new_behavior_code = '04 16 00 00' # 4=display a msg, 16=msg code bits 3/4 not used
        for addr in e_1F_to_4F:
            f.seek(addr)
            f.write(binascii.unhexlify(new_behavior_code.replace(' ','')))
        for addr in e_4F_8F:
            f.seek(addr)
            f.write(binascii.unhexlify(new_behavior_code.replace(' ','')))


    def boost_ep(f, multiplier):
        multiplier = int(multiplier) # comes from html as string which messes up the multiplication, it will concat instead
        starting_addr = 0x14079
        num_enemies = 101
        for i in range(num_enemies):
            # ep value is stored in decimal
            f.seek(starting_addr)
            ep = int(binascii.hexlify(f.read(6)), 10)
            ep = ep * multiplier
            # pad with zeros to take up 6 bytes space
            ep = str(ep).rjust(12, '0')
            # if we have some overflow just trim it off
            ep = ep[-12:] # only use rightmost 12 chars
            # go back to address, read operation moved our pointer
            f.seek(starting_addr)
            f.write(binascii.unhexlify(ep))
            starting_addr = starting_addr + 128


    def generate_map(f):
        maps = 'KEY\n# = wall\n| = door\nR = room\n\n'
        levels = [0x11A50, 0x11BE0, 0x11D70, 0x11F00, 0x12090, 0x12220, 0x123B0, 0x12540, 0x126D0]
        maze, hex_data = make_map(20, 20, paths=[
            {'start':(0,0), 'end':(0,10)},
            {'start':(0,0), 'end':(13,3)},
            {'start':(0,0), 'end':(13,18)}
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
            {'start':(12,7), 'end':(4,16)},
            {'start':(12,7), 'end':(10,8)},
            {'start':(12,7), 'end':(12,4)},
            {'start':(4,16), 'end':(9,18)},
            {'start':(9,18), 'end':(16,15)}
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
            {'start':(15,11), 'end':(1,8)},
            {'start':(15,11), 'end':(10,8)}
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
            {'start':(10,18), 'end':(17,7)},
            {'start':(10,18), 'end':(11,10)},
            {'start':(10,0), 'end':(10,8)}
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
            {'start':(0,0), 'end':(8,8)},
            {'start':(10,0), 'end':(8,8)}
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

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(8,8), 'end':(9,18)},
            {'start':(10,0), 'end':(9,18)}
            ])
        maps += 'B6F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[5])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(0,19), 'end':(11,8)},
            {'start':(10,0), 'end':(11,8)}
            ])
        maps += 'B7F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[6])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            ])
        maps += 'B8F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        f.seek(levels[7])
        f.write(binascii.unhexlify(hex_data))

        maze, hex_data = make_map(20, 20, paths=[
            {'start':(10,0), 'end':(8,2)}
            ])
        maps += 'B9F\n'
        for row in maze:
            for cell in row:
                maps += cell
                maps += ' '
            maps += '\n'
        maps += '\n'
        # with open('MAPS.txt','w') as m:
        #     m.write(maps)
        f.seek(levels[8])
        f.write(binascii.unhexlify(hex_data))
        return maps



    # put all keys into a list so we can shuffle them around
    shuffled_items = list(key_items.keys())
    random.shuffle(shuffled_items)

    shuffled_stairs = list(stairs.keys())
    random.shuffle(shuffled_stairs)

    # make new dictionary of shuffled items paired with original address/values
    shuffled_item_dict = dict(zip(shuffled_items, key_items.values()))
    shuffled_stair_dict = dict(zip(shuffled_stairs, stairs.values()))
    # print(shuffled_stair_dict)
    with open(rom, 'r+b') as f:
        shuffle_chars(f)
        if easy_spells == 'True':
            change_spell_names(f)
        if custom_text == 'True':
            customize_text(f)
        if stair_shuffle == 'True':
            for stair in stairs:
                addr = stairs[stair]['address']
                val = shuffled_stair_dict[stair]['value']
                raddr = shuffled_stair_dict[stair]['raddr']
                rval = stairs[stair]['rvalue']
                name = shuffled_stair_dict[stair]['name']
                coord = stairs[stair]['coord']
                spoiler += f'{name} at {coord}\n'
                f.seek(addr)
                f.write(binascii.unhexlify(val.replace(' ',''))) # write value without spaces
                # this is so that you can backtrack up the stairs you just went down
                f.seek(raddr)
                f.write(binascii.unhexlify(rval.replace(' ',''))) # write value without spaces
            spoiler += '=\n'
        if key_shuffle == 'True':
            for item in key_items:
                addr = key_items[item]['address'] # original address
                val = shuffled_item_dict[item]['value'] # shuffled value
                coord = key_items[item]['coord']
                name = shuffled_item_dict[item]['name']
                spoiler += f'{name} at {coord}\n'
                f.seek(addr) # go to address
                f.write(binascii.unhexlify(val.replace(' ',''))) # write value without spaces
        for address in fixed_encounters:
            monster_id = random.randint(0,100)
            hex_id = '{:02x}'.format(monster_id)
            spoiler += f'Murphy\'s ghost is now monster ID {monster_id}\n'
            f.seek(address)
            f.write(binascii.unhexlify(hex_id.replace(' ','')))
        if shop_shuffle == 'True':
            shuffle_shop(f)
        if curse_shuffle == 'True':
            shuffle_curses(f)
        if buff_coins == 'True':
            address = 0x14655
            value = '03 03'  # buff coins 3d3 HP (i think)
            f.seek(address)
            f.write(binascii.unhexlify(value.replace(' ','')))
        if disable_elevator == 'True':
            disable_elevators(f)
        if infinite_potions == 'True':
            make_potions_reusable(f)
        if ep_multiplier != '1':
            boost_ep(f, ep_multiplier)
        if monster_shuffle == 'True':
            shuffle_monsters(f)
        if proc_gen_map == 'True':
            maps = generate_map(f)
    return rom, spoiler, maps
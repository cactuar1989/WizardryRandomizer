import shutil
from map_maker import make_map
from rando import randomize_pgotmo
from kod_rando import randomize_kod
from lol_rando import randomize_lol
from ng3_rando import randomize_ng3


def main():
    log = ''

    # copy roms so we don't alter the original
    shutil.copyfile('PGOTMO.nes', 'PGOTMO_test.nes')
    shutil.copyfile('KOD.nes', 'KOD_test.nes')
    shutil.copyfile('LOL.nes', 'LOL_test.nes')
    shutil.copyfile('ng3.nes', 'ng3_test.nes')
    
    # common options
    seed = 'test_seed'

    rando_rom = randomize_ng3(
        rom='ng3_test.nes',
        normal_game='False',
        skin='35',
        clothes='22',
        outline='07',
        starting_health=100,
        starting_lives=0,
        starting_continues=10,
        windmill=1,
        fire_wheel=1,
        dragon_balls=1,
        vacuum=1,
        invincible=1,
        drop_shuffle='True',
        enemy_shuffle='False',
        boss_shuffle='False',
        level_shuffle='False',
        debug_mode='False',
        skip_cutscenes='True',
        seed=seed)
    # log += ('NG3\n' + spoiler + '\n')

    # rando_rom, spoiler, maps, = randomize_pgotmo(
    #     rom='ROMS/PGOTMO_test.nes', 
    #     custom_text='True',
    #     easy_spells='True',
    #     key_shuffle='True',
    #     stair_shuffle='True', 
    #     curse_shuffle='True', 
    #     shop_shuffle='True',
    #     buff_coins='True',
    #     disable_elevator='True',
    #     infinite_potions='False',
    #     ep_multiplier='5',
    #     monster_shuffle='True',
    #     proc_gen_map='True',
    #     seed=seed
    #     )
    # log += ('PGOTMO\n' + spoiler + '\n' + maps + '\n')

    # rando_rom, spoiler, maps = randomize_kod(
    #     rom='ROMS/KOD_test.nes',
    #     custom_text='True',
    #     easy_spells='True',
    #     stair_shuffle='True',
    #     key_shuffle='True', 
    #     curse_shuffle='True',
    #     shop_shuffle='True',
    #     ep_multiplier='5',
    #     monster_shuffle='True',
    #     boss_shuffle='True', 
    #     proc_gen_map='True',
    #     seed=seed
    #     )
    # log += ('KOD\n' + spoiler + '\n' + maps + '\n')

    # rando_rom, spoiler, maps = randomize_lol(
    #     rom='ROMS/LOL_test.nes',
    #     default_language='english',
    #     custom_text='True',
    #     easy_spells='False',
    #     stair_shuffle='False',
    #     key_shuffle='False',
    #     curse_shuffle='False',
    #     shop_shuffle='False',
    #     # mortal_lkbreth='True',
    #     ep_multiplier='1',
    #     monster_shuffle='False',
    #     boss_shuffle='False', 
    #     proc_gen_map='False',
    #     seed=seed
    #     )
    # log += ('LOL\n' + spoiler + '\n' + maps + '\n')

    with open('test_rando_log.txt', 'w') as f:
        f.write(log)


if __name__ == '__main__':
    main()
import os
import random
import string
import zipfile
from flask import Flask, render_template, request, send_file
from flask_caching import Cache
from rando import randomize_pgotmo
from kod_rando import randomize_kod
from lol_rando import randomize_lol
from ng3_rando import randomize_ng3


config = {
    'DEBUG': True,
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
}
app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


# SSL Domain Control Validation
@app.route('/.well-known/pki-validation/7E6C0128130919B81FBE5DABF09D079E.txt')
def dcv():
    with open('7E6C0128130919B81FBE5DABF09D079E.txt') as f:
        text = f.read()
    return text


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/lost')
def lost():
    return render_template('lost.html')


@app.route('/pgotmo')
def pgotmo():
    return render_template('pgotmo.html')
@app.route('/kod')
def kod():
    return render_template('kod.html')
@app.route('/lol')
def lol():
    return render_template('lol.html')
@app.route('/ng3')
def ng3():
    return render_template('ng3.html')

@app.route('/cleanup')
def cleanup():
    errors = 'None'
    zip_num = len(os.listdir('ZIPS'))
    zip_size = 0
    for path, dirs, files in os.walk('ZIPS'):
        for f in files:
            fp = os.path.join(path, f)
            zip_size += os.path.getsize(fp)
    rom_num = len(os.listdir('ROMS'))
    rom_size = 0
    for path, dirs, files in os.walk('ROMS'):
        for f in files:
            fp = os.path.join(path, f)
            rom_size += os.path.getsize(fp)
    try:
        for f in os.listdir('ZIPS'):
            os.remove(os.path.join('ZIPS', f))
        for f in os.listdir('ROMS'):
            os.remove(os.path.join('ROMS', f))
    except Exception as e:
        errors = e
    out = f'''
    Files in /ZIPS: {zip_num}
    Size of /ZIPS: {zip_size}
    Files in /ROMS: {rom_num}
    Size of /ROMS: {rom_size}
    Errors: {errors}
    '''
    return(out)

@app.route('/count')
def count():
    DIR = 'ROMS'
    count = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    return(f'Files in {DIR}:{count}')


@app.route('/test_page')
def test_page():
    return render_template('test_page.html')
@app.route('/test_upload', methods = ['GET', 'POST'])
def test_upload():
    if request.method == 'POST':
        return request.form


@app.route('/pgotmo_upload', methods = ['GET', 'POST'])
def pgotmo_upload():
    # random 10 letters
    seed = (''.join(random.choice(string.ascii_letters) for i in range(10)))
    if request.method == 'POST':
        custom_text = request.form.get('custom_text')
        easy_spells = request.form.get('easy_spells')
        stair_shuffle = request.form.get('stair_shuffle')
        key_shuffle = request.form.get('key_shuffle')
        curse_shuffle = request.form.get('curse_shuffle')
        shop_shuffle = request.form.get('shop_shuffle')
        buff_coins = request.form.get('buff_coins')
        disable_elevator = request.form.get('disable_elevator')
        infinite_potions = 'False'
        ep_multiplier = request.form['boost_experience']
        monster_shuffle = request.form.get('monster_shuffle')
        proc_gen_map = request.form.get('proc_gen_map')

        f = request.files['file']
        if f.filename != '':
            if f.filename[-4:].lower() != '.nes':
                return render_template('error.html',msg='That is NOT a .nes file')
            # # increment number file
            # with open('number.txt','r') as n:
            #     count = int(n.read())
            # count += 1
            # with open('number.txt','w') as n:
            #     n.write(str(count))
            f.save(f'ROMS/PGOTMO_{seed}.nes')
            try:
                rando_rom, spoiler, maps = randomize_pgotmo(
                    rom=f'ROMS/PGOTMO_{seed}.nes', 
                    custom_text=custom_text,
                    easy_spells=easy_spells,
                    key_shuffle=key_shuffle,
                    stair_shuffle=stair_shuffle, 
                    curse_shuffle=curse_shuffle, 
                    shop_shuffle=shop_shuffle,
                    buff_coins=buff_coins,
                    disable_elevator=disable_elevator,
                    infinite_potions=infinite_potions,
                    ep_multiplier=ep_multiplier,
                    monster_shuffle=monster_shuffle,
                    proc_gen_map=proc_gen_map,
                    seed=seed
                    )
            except:
                return render_template('error.html',msg='Rom error. Was this the US version?')
            with zipfile.ZipFile(f'ZIPS/PGOTMO_{seed}.zip', mode='w') as zipfolder:
                zipfolder.write(rando_rom)
                with open(f'ZIPS/spoiler_{seed}.txt', 'w') as s:
                    s.write(spoiler)
                zipfolder.write(f'ZIPS/spoiler_{seed}.txt')
                if len(maps) > 0:
                    with open(f'ZIPS/maps_{seed}.txt', 'w') as m:
                        m.write(maps)
                    zipfolder.write(f'ZIPS/maps_{seed}.txt')
            return send_file(f'ZIPS/PGOTMO_{seed}.zip', download_name=f'PGOTMO_{seed}.zip')
        else:
            return render_template('pgotmo.html')
    else:
        return render_template('pgotmo.html')


@app.route('/kod_upload', methods = ['GET', 'POST'])
def kod_upload():
    # random 10 letters
    seed = (''.join(random.choice(string.ascii_letters) for i in range(10)))
    if request.method == 'POST':
        custom_text = request.form.get('custom_text')
        easy_spells = request.form.get('easy_spells')
        stair_shuffle = request.form.get('stair_shuffle')
        key_shuffle = request.form.get('key_shuffle')
        curse_shuffle = request.form.get('curse_shuffle')
        shop_shuffle = request.form.get('shop_shuffle')
        monster_shuffle = request.form.get('monster_shuffle')
        boss_shuffle = request.form.get('boss_shuffle')
        ep_multiplier = request.form['boost_experience']
        proc_gen_map = request.form.get('proc_gen_map')
        f = request.files['file']
        if f.filename != '':
            if f.filename[-4:].lower() != '.nes':
                return render_template('error.html',msg='That is NOT a .nes file')
            # # increment number file
            # with open('kod_number.txt','r') as n:
            #     count = int(n.read())
            # count += 1
            # with open('kod_number.txt','w') as n:
            #     n.write(str(count))
            f.save(f'ROMS/KOD_{seed}.nes')
            try:
                rando_rom, spoiler, maps = randomize_kod(
                    rom=f'ROMS/KOD_{seed}.nes',
                    custom_text=custom_text,
                    easy_spells=easy_spells,
                    stair_shuffle=stair_shuffle,
                    key_shuffle=key_shuffle, 
                    curse_shuffle=curse_shuffle,
                    shop_shuffle=shop_shuffle,
                    ep_multiplier=ep_multiplier,
                    monster_shuffle=monster_shuffle,
                    boss_shuffle=boss_shuffle, 
                    proc_gen_map=proc_gen_map,
                    seed=seed
                    )
            except:
                return render_template('error.html',msg='Rom error. Was this the US version?')
            with zipfile.ZipFile(f'ZIPS/KOD_{seed}.zip', mode='w') as zipfolder:
                zipfolder.write(rando_rom)
                with open(f'ZIPS/kod_spoiler_{seed}.txt','w') as s:
                    s.write(spoiler)
                zipfolder.write(f'ZIPS/kod_spoiler_{seed}.txt')
                if len(maps) > 0:
                    with open(f'ZIPS/kod_maps_{seed}.txt', 'w') as m:
                        m.write(maps)
                    zipfolder.write(f'ZIPS/kod_maps_{seed}.txt')
            return send_file(f'ZIPS/KOD_{seed}.zip', download_name=f'KOD_{seed}.zip')
        else:
            return render_template('kod.html')
    else:
        return render_template('kod.html')


@app.route('/lol_upload', methods = ['GET', 'POST'])
def lol_upload():
    # random 10 letters
    seed = (''.join(random.choice(string.ascii_letters) for i in range(10)))
    if request.method == 'POST':
        default_language = request.form['default_language']
        custom_text = request.form.get('custom_text')
        easy_spells = request.form.get('easy_spells')
        stair_shuffle = request.form.get('stair_shuffle')
        key_shuffle = request.form.get('key_shuffle')
        curse_shuffle = request.form.get('curse_shuffle')
        shop_shuffle = request.form.get('shop_shuffle')
        monster_shuffle = request.form.get('monster_shuffle')
        boss_shuffle = request.form.get('boss_shuffle')
        # mortal_lkbreth = request.form.get('mortal_lkbreth')
        ep_multiplier = request.form['boost_experience']
        proc_gen_map = request.form.get('proc_gen_map')
        f = request.files['file']
        if f.filename != '':
            if f.filename[-4:].lower() != '.nes':
                return render_template('error.html',msg='That is NOT a .nes file')
            # # increment number file
            # with open('lol_number.txt','r') as n:
            #     count = int(n.read())
            # count += 1
            # with open('lol_number.txt','w') as n:
            #     n.write(str(count))
            f.save(f'ROMS/LOL_{seed}.nes')
            try:
                rando_rom, spoiler, maps = randomize_lol(
                    rom=f'ROMS/LOL_{seed}.nes',
                    default_language=default_language,
                    custom_text=custom_text,
                    easy_spells=easy_spells,
                    stair_shuffle=stair_shuffle,
                    key_shuffle=key_shuffle, 
                    curse_shuffle=curse_shuffle,
                    shop_shuffle=shop_shuffle,
                    ep_multiplier=ep_multiplier,
                    monster_shuffle=monster_shuffle,
                    boss_shuffle=boss_shuffle,
                    # mortal_lkbreth=mortal_lkbreth, 
                    proc_gen_map=proc_gen_map,
                    seed=seed
                    )
            except:
                return render_template('error.html',msg='Rom error. Was this the correct game?')
            with zipfile.ZipFile(f'ZIPS/LOL_{seed}.zip', mode='w') as zipfolder:
                zipfolder.write(rando_rom)
                with open(f'ZIPS/lol_spoiler_{seed}.txt','w') as s:
                    s.write(spoiler)
                zipfolder.write(f'ZIPS/lol_spoiler_{seed}.txt')
                if len(maps) > 0:
                    with open(f'ZIPS/lol_maps_{seed}.txt', 'w') as m:
                        m.write(maps)
                    zipfolder.write(f'ZIPS/lol_maps_{seed}.txt')
            return send_file(f'ZIPS/LOL_{seed}.zip', download_name=f'LOL_{seed}.zip')
        else:
            return render_template('lol.html')
    else:
        return render_template('lol.html')

@app.route('/ng3_upload', methods = ['GET', 'POST'])
def ng3_upload():
    # random 10 letters
    seed = (''.join(random.choice(string.ascii_letters) for i in range(10)))
    if request.method == 'POST':
        skin = request.form['skin']
        clothes = request.form['clothes']
        outline = request.form['outline']
        starting_health = int(request.form['starting_health'])
        starting_lives = int(request.form['starting_lives'])
        starting_continues = int(request.form['starting_continues'])
        # custom ninpo costs not implemented yet
        windmill = 10
        fire_wheel = 8
        dragon_balls = 8
        vacuum = 10
        invincible = 20
        drop_shuffle = request.form.get('drop_shuffle')
        enemy_shuffle = request.form.get('enemy_shuffle')
        level_shuffle = request.form.get('level_shuffle')
        boss_shuffle = request.form.get('boss_shuffle')
        debug_mode = 'False'
        skip_cutscenes = 'True'
        f = request.files['file']
        # print(f'HEALTH: {starting_health}')
        if f.filename != '':
            if f.filename[-4:].lower() != '.nes':
                return render_template('error.html',msg='That is NOT a .nes file')
            f.save(f'ROMS/ng3_{seed}.nes')
            try:
                rando_rom = randomize_ng3(
                    rom=f'ROMS/ng3_{seed}.nes',
                    normal_game='False',
                    skin=skin,
                    clothes=clothes,
                    outline=outline,
                    starting_health=starting_health,
                    starting_lives=starting_lives,
                    starting_continues=starting_continues,
                    # custom ninpo costs not implemented yet
                    windmill=10,
                    fire_wheel=8,
                    dragon_balls=8,
                    vacuum=10,
                    invincible=20,
                    drop_shuffle=drop_shuffle,
                    enemy_shuffle=enemy_shuffle,
                    boss_shuffle=boss_shuffle,
                    level_shuffle=level_shuffle,
                    debug_mode='False',
                    skip_cutscenes='True',
                    seed=seed)
            except Exception as e:
                return render_template('error.html',msg=f'Rom error. Was this the correct game? Server msg: {e}')
            return send_file(f'ROMS/ng3_{seed}.nes', download_name=f'ng3_{seed}.nes')
        else:
            return render_template('ng3.html')
    else:
        return render_template('ng3.html')


@app.route('/error')
def error():
    return render_template('error.html', msg=msg)


if __name__ == '__main__':
    app.run()
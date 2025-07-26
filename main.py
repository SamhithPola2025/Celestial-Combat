from ursina import *
import math

app = Ursina()

camera.orthographic = True
camera.fov = 10

menu_parent = Entity()
settings_menu = Entity(enabled=False)
grass_entities = []
fight_window = Entity(parent=camera.ui, enabled=False)
fight_text = Text('Battle!', parent=fight_window, y=0.2, scale=3, enabled=True)
run_btn = Button(text='Skidaddle', parent=fight_window, y=-0.3, scale=(2,1), enabled=True)
attack_button = Button(text='Attack', parent=fight_window, y=-0.1, scale=(2,1), enabled=True)
player_health = 100
enemy_health = 100
fight_active = False

wandering_trader_not_minecraft_stolen_dont_sue_me = Entity(model='quad', color=color.green, scale=(0.3, 0.5), position=(3,3,1), z=1, enabled=True, collider='box')
grassinstance = Entity(model='quad', z=1, color=color.green, scale=(0.05, 0.1), y=-0.25, enabled=True, collider='box')
player = Entity(model='quad', z=1, color=color.orange, scale=(0.3, 0.5), y=1, enabled=True, collider='box')

playerspeed = 5

background2 = Entity(model='quad', z=-100, scale=(50, 30), color=color.hex("#615F3C"), enabled=False)
background = Panel(
    parent=menu_parent,
    scale=999,
    color=color.hex('#218eb4'),
    z=1  
)

music_files = [
    r'music/ready-set-drift-michael-grubb-main-version-24555-02-59.mp3',
    r'music/space-ranger-moire-main-version-03-04-10814.mp3',
    r'music/easy-arcade-hartzmann-main-version-28392-02-32.mp3'
]

def start_fight():
    global fight_active
    fight_active = True
    fight_window.enabled = True
    player.enabled = False
    fight_text.text = "Battle! Enemy HP: " + str(enemy_health)

def end_fight():
    global fight_active
    fight_active = False
    fight_window.enabled = False
    player.enabled = True

def attack():
    global enemy_health
    enemy_health -= 20
    fight_text.text = f'Enemy health: {enemy_health}'
    if enemy_health <= 0:
        fight_text.text = "You Win!"
        invoke(end_fight, delay=1)

def run():
    fight_text.text = "You ran away!"
    invoke(end_fight, delay=1)

attack_button.on_click = attack
run_btn.on_click = run

music_index = 0
current_music = None
volume_slider = None

def grassgen(num_grass=20, area_size=50):
    global grass_entities
    for g in grass_entities:
        destroy(g)
    grass_entities.clear()
    for _ in range(num_grass):
        x = random.uniform(-area_size, area_size)
        y = random.uniform(-area_size, area_size)
        grass = Entity(
            model='quad',
            color=color.green,
            scale=(0.05, 0.1),
            position=(x, y, 0),
            rotation_z=random.uniform(-20, 20),
            collider='box'
        )
        grass_entities.append(grass)

def play_next_song():
    global music_index, current_music

    if current_music:
        destroy(current_music)

    current_file = music_files[music_index]
    current_music = Audio(current_file, autoplay=True)
    current_music.volume = volume_slider.value if volume_slider else 0.5

    def check_end():
        global music_index
        if current_music and not current_music.playing:
            music_index = (music_index + 1) % len(music_files)
            play_next_song()

    current_music.update = check_end

def tradercode(move_distance=3, speed=2):
    wandering_trader_not_minecraft_stolen_dont_sue_me.position = (player.x, player.y + 2, 0)
    wandering_trader_not_minecraft_stolen_dont_sue_me.enabled = True
    wandering_trader_not_minecraft_stolen_dont_sue_me.base_x = player.x
    wandering_trader_not_minecraft_stolen_dont_sue_me.base_y = player.y + 2

    def trader_update():
        t = time.time() * speed
        offset = math.sin(t) * move_distance
        wandering_trader_not_minecraft_stolen_dont_sue_me.x = wandering_trader_not_minecraft_stolen_dont_sue_me.base_x + offset
        wandering_trader_not_minecraft_stolen_dont_sue_me.y = wandering_trader_not_minecraft_stolen_dont_sue_me.base_y

    wandering_trader_not_minecraft_stolen_dont_sue_me.update = trader_update

def start_game():
    global enemy_health, player_health
    menu_parent.enabled = False
    player.enabled = True
    grassinstance.enabled = True
    camera.position = (player.x, player.y, -10)
    background2.enabled = True
    background.enabled = False
    grassgen(150, 12)
    wandering_trader_not_minecraft_stolen_dont_sue_me.enabled = True
    tradercode()
    enemy_health = 100
    player_health = 100
    fight_window.enabled = False

def quit_game():
    application.quit()

def open_settings():
    menu_parent.enabled = False
    settings_menu.enabled = True

def back_to_menu():
    settings_menu.enabled = False
    menu_parent.enabled = True

def LoadMainMenu():
    Text("Celestial Combat", parent=menu_parent, scale=35, y=3.5, x=-3.75, z=0, font='Bitcountprop.ttf')
    Text("V1.1", parent=menu_parent, scale=30, y=2.5, x=-0.75, z=0, font='Bitcountprop.ttf')

    start_btn = Button(text='Start', scale=(2.5, 1), y=1, parent=menu_parent, on_click=start_game)
    start_btn.text_entity.font = 'Bitcountprop.ttf'

    settings_btn = Button(text='Settings', scale=(2.5, 1), y=-0.5, parent=menu_parent, on_click=open_settings)
    settings_btn.text_entity.font = 'Bitcountprop.ttf'

    quit_btn = Button(text='Quit', scale=(2.5, 1), y=-2, parent=menu_parent, on_click=quit_game)
    quit_btn.text_entity.font = 'Bitcountprop.ttf'

def LoadSettingsMenu():
    global volume_slider, current_music

    Text("Settings", parent=settings_menu, scale=35, y=2, x=-2, z=0, font='Bitcountprop.ttf')

    volume_slider = Slider(scale=20, min=0, max=10, default=0.5, step=0.1, y=0.1, x=-5, parent=settings_menu)

    def on_volume_change():
        if current_music:
            current_music.volume = volume_slider.value

    volume_slider.on_value_changed = on_volume_change

    Text("Volume", parent=settings_menu, y=-0.5, scale=10, z=0, x=-0.5, font='Bitcountprop.ttf')

    back_btn = Button(text='Back', scale=(2.5, 1.5), y=-2, parent=settings_menu, on_click=back_to_menu)
    back_btn.text_entity.font = 'Bitcountprop.ttf'

def update():

    print("update")
    print('player enabled:', player.enabled)
    print('trader enabled:', wandering_trader_not_minecraft_stolen_dont_sue_me.enabled)

    if player.enabled and wandering_trader_not_minecraft_stolen_dont_sue_me.enabled and not fight_active:
        if player.intersects(wandering_trader_not_minecraft_stolen_dont_sue_me).hit:
            start_fight()

    if player.enabled:
        x = held_keys['d'] - held_keys['a']
        y = held_keys['w'] - held_keys['s']
        move = Vec2(x, y)

        speed = playerspeed

        for grass in grass_entities:
            if player.intersects(grass).hit:
                speed *= 0.6
                print("hit")
                break

        if move.length() > 0:
            move = move.normalized() * speed * time.dt
            player.position += Vec3(move.x, move.y, 0)
            player.rotation_z = lerp(player.rotation_z, x * 10, time.dt * 10)
        else:
            player.rotation_z = lerp(player.rotation_z, 0, time.dt * 10)
        camera.position = lerp(camera.position, (player.x, player.y, -10), time.dt * 5)
        background2.position = Vec3(camera.position.x, camera.position.y, background2.z)

LoadMainMenu()
LoadSettingsMenu()
play_next_song()

window.title = 'Celestial-Combat V1.1'
window.borderless = False
window.fullscreen = True

app.run()
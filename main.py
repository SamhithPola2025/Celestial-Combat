from ursina import *
import random, math, time

app = Ursina()

camera.orthographic = True
camera.fov = 10

menu_parent = Entity()
settings_menu = Entity(enabled=False)
grass_entities = []
fight_window = Entity(parent=camera.ui, enabled=False, z=10)
coins = 10
wandering_traders = []
current_enemy = None
better_fireball_counter = 0
fireball_damage = 25

shop_panel = Panel(
    color=color.hex("#C0D1D2"),
    parent=camera.ui,
    x=0,
    y=0,
    scale=(4,4),
    enabled=False,
)

# Create the coins counter text
coinscounter = Text(
    text=f'Coins: {coins}',
    parent=shop_panel,
    scale=0.5,
    x=-0.1,          
    y=-0.1,        
    origin=(0, 0),
    font='Bitcountprop.ttf',
    z=-1
)

print(f'coins: {coins}')

shop_opciones_uno = Button(
    text=(f'Stronger fireball: Cost: 10 Used: {better_fireball_counter}'),
    scale=(0.1,0.05),
    x=-0.15,
    y=0.07,
    parent=shop_panel,  # CHANGED: Parent to shop_panel instead of camera.ui
    color=color.hex("#35752A"),
    highlight_color=color.lime,
    pressed_color=color.orange,
    enabled=False,
    z=-0.1,  # ADDED: Set z-index to render above the panel
    font='Bitcountprop.ttf'
)

def open_shop():
    # Update the coins text before showing the shop
    coinscounter.text = f'Coins: {coins}'
    shop_panel.enabled = True
    print(f"Shop opened! Coins: {coins}")  # Debug print
    shop_opciones_uno.enabled=True
    
def increased_fireball():
    global coins, better_fireball_counter
    if coins >= 10:
        coins -= 10
        better_fireball_counter += 1
        print(better_fireball_counter)

shop_opciones_uno.on_click = increased_fireball

shop_button = Button(
    text='Shop',
    parent=camera.ui,
    x=-0.7,
    y=-0.4,
    scale=(0.2, 0.1),
    color=color.hex("#BD9A27"),
    highlight_color=color.yellow,
    font='Bitcountprop.ttf',
    enabled=True,
    visible=True,
    z=-0.1
)
shop_button.on_click = open_shop

# Add a function to update coins
def add_coins(amount):
    global coins
    coins += amount
    coinscounter.text = f'Coins: {coins}'
    print(f"Added {amount} coins. Total: {coins}")

fight_text = Text(
    'Battle!',
    parent=fight_window,
    y=0.35,
    scale=2,
    origin=(0, 0),
    color=color.white,
    font='Bitcountprop.ttf',
)
wins = 0
top_wins_counter = Text(
    f"Wins: {wins}",
    origin=(0.5, -0.5),
    position=(0.8, 0.45),
    scale=2,
    font='Bitcountprop.ttf',
)
close_shop = Button(
    text='Close',
    parent=shop_panel,
    color=color.hex("#6E8B2B"),
    scale=(0.1,0.05),
    x = 0.14,
    y = -0.08,
    z = -0.1,
)

def on_close_shop():
    shop_panel.enabled=False

close_shop.on_click = on_close_shop

fight_background = Panel(
    parent=fight_window,
    scale=400,
    z=60,
    color=color.blue,
    enabled=False
)

# ----- fight buttons -----
attackoptionsdialogue = Panel(
    parent=fight_window,
    enabled=False,
    scale=(0.8, 0.3),
    color=color.hex("#333333aa"),
    y=-0.3
)

# skip turn button
attack1button = Button(
    parent=attackoptionsdialogue,
    enabled=False,
    scale=(0.25, 0.2),
    color=color.hex("#228761"),
    text='Skip',
    font='VeraMono.ttf',
    x=-0.3,
)

# fire ball button
attack2button = Button(
    parent=attackoptionsdialogue,
    enabled=False,
    scale=(0.25, 0.2),
    color=color.hex("#22b12c"),
    text='Fire Ball',
    font='VeraMono.ttf',
)

# push button
attack3button = Button(
    parent=attackoptionsdialogue,
    enabled=False,
    scale=(0.25, 0.2),
    color=color.hex("#b1a022"),
    text='Push',
    font='VeraMono.ttf',
    x=0.3,
)


attack_button = Button(
    text='Attack',
    parent=fight_window,
    y=-0.1,
    x=-0.4,
    scale=(0.4,0.4),
    color=color.azure,
    highlight_color=color.light_gray,
    pressed_color=color.blue,
)

run_button = Button(
    text='Run',
    parent=fight_window,
    y=-0.1,
    x=0.4,
    scale=(0.4,0.4),
    color=color.red,
    highlight_color=color.light_gray,
    pressed_color=color.blue,
)

fight_window.z = 100
fight_text.z = 0.1
attack_button.z = 0.1
run_button.z = 0.1

player = Entity(model='quad', texture='sprites/player', scale=(0.8, 1), y=1,
                collider='box', enabled=False)

playerspeed = 5
player_health = 100
enemy_health = 100
fight_active = False
player_turn = True

player_health_text = Text(
    f"Player HP: {player_health}",
    origin=(0.5, -0.5),
    position=(0.15, 0.45),
    scale=2,
    font='Bitcountprop.ttf'
)

def start_fight(enemy):
    global fight_active, player_turn, player_health, enemy_health, current_enemy
    current_enemy = enemy
    fight_active = True
    fight_window.enabled = True
    player.enabled = False
    fight_background.enabled = True
    top_wins_counter.enabled = False

    player_health = 100
    enemy_health = 100
    player_health_text.text = f"Player HP: {player_health}"
    fight_text.text = f"Battle! Enemy HP: {enemy_health}"
    player_turn = True
    attackoptionsdialogue.enabled = False

def spawn_wandering_traders(num_traders=3, area_size=12):
    global wandering_traders
    for trader in wandering_traders:
        destroy(trader)
    wandering_traders.clear()

    for _ in range(num_traders):
        trader = Entity(
            model = 'quad',
            texture ='sprites/enemy',
            scale=(0.8,0.9),
            position=Vec3(
                random.uniform(-area_size, area_size),
                random.uniform(-area_size, area_size),
                0
            ),
            collider='box'
        )
        trader.home_pos = Vec2(trader.x, trader.y)
        trader.dir = Vec2(random.uniform(-1, 1), random.uniform(-1, 1)).normalized()
        trader.speed = random.uniform(1,3)
        wandering_traders.append(trader)

def update_traders(move_distance=1.5, speed=1):
    for trader in wandering_traders:
        trader.position += Vec3(trader.dir.x, trader.dir.y, 0) * trader.speed * time.dt
        if random.random() < 0.03:
            trader.dir = Vec2(random.uniform(-1, 1), random.uniform(-1, 1)).normalized()
        offset = Vec2(trader.x, trader.y) - trader.home_pos
        max_dist=5
        if offset.length() > max_dist:
            trader.dir = (-offset).normalized()
                             
def end_fight():
    global fight_active
    fight_active = False
    fight_window.enabled = False
    player.enabled = True
    attackoptionsdialogue.enabled = False
    top_wins_counter.enabled = True
    top_wins_counter.text = f"Wins: {wins}"

def attack_player_move(attack_type):
    global enemy_health, player_turn, coins, current_enemy
    if not player_turn:
        return

    if attack_type == "skip":
        print("Player skipped turn")
    elif attack_type == "fire":
        enemy_health -= fireball_damage
    elif attack_type == "push":
        enemy_health -= 10

    fight_text.text = f"Enemy health: {max(enemy_health,0)}"
    attackoptionsdialogue.enabled = False

    if enemy_health <= 0:
        fight_text.text = "You Win!"
        global wins
        wins += 1
        add_coins(10)
        print(f"wins: {wins}, wins updated")
        
        if current_enemy:
            die(current_enemy)
            wandering_traders.remove(current_enemy)
            current_enemy = None

        invoke(end_fight, delay=1)
        return

    player_turn = False
    invoke(enemy_turn, delay=1)

def enemy_turn():
    global player_health, player_turn
    damage = random.randint(5, 15)
    player_health -= damage
    player_health_text.text = f"Player HP: {max(player_health,0)}"
    fight_text.text = f"Enemy attacks! Player takes {damage} damage"

    if player_health <= 0:
        fight_text.text = "You Lose!"
        invoke(end_fight, delay=1)
        return

    player_turn = True

attack1button.on_click = lambda: attack_player_move("skip")
attack2button.on_click = lambda: attack_player_move("fire")
attack3button.on_click = lambda: attack_player_move("push")

def attack_button_click():
    if fight_active and player_turn and not attackoptionsdialogue.enabled:
        attackoptionsdialogue.enabled = True
        attack1button.enabled = True
        attack2button.enabled = True
        attack3button.enabled = True
    elif attackoptionsdialogue.enabled:
        attackoptionsdialogue.enabled = False
        attack1button.enabled = False
        attack2button.enabled = False
        attack3button.enabled = False

attack_button.on_click = attack_button_click

def run():
    fight_text.text = "You ran away!"
    invoke(end_fight, delay=1)

run_button.on_click = run

music_files = [
    'music/ready-set-drift-michael-grubb-main-version-24555-02-59.mp3',
    'music/space-ranger-moire-main-version-03-04-10814.mp3',
    'music/easy-arcade-hartzmann-main-version-28392-02-32.mp3'
]
music_index = 0
current_music = None
volume_slider = None

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

def grassgen(num_grass=20, area_size=50):
    global grass_entities
    for g in grass_entities: destroy(g)
    grass_entities.clear()
    for _ in range(num_grass):
        x = random.uniform(-area_size, area_size)
        y = random.uniform(-area_size, area_size)
        grass = Entity(model='quad', color=color.green, scale=(0.05, 0.1),
                       position=(x, y, 0), rotation_z=random.uniform(-20, 20),
                       collider='box')
        grass_entities.append(grass)

def die(entity):
    entity.color = color.gray
    for i in range(10):
        p = Entity(
            model='quad',
            color=color.brown,
            scale=0.1,
            position=entity.position,
            eternal=False,
        )
        p.animate_position(entity.position + Vec3(random.uniform(-1,1), random.uniform(-1,1), 0), duration=0.5)
        p.fade_out(0.5)

    destroy(entity)


def start_game():
    menu_parent.enabled = False
    player.enabled = True
    camera.position = (player.x, player.y, -10)
    
    # enable the background
    background2.enabled = True
    background.enabled = False
    
    # generate grass
    grassgen(150, 12)
    
    # spawn wandering traders
    spawn_wandering_traders(num_traders=3, area_size=12)
    
    # hide fight window and enable wins counter
    fight_window.enabled = False
    top_wins_counter.enabled = True

def quit_game(): application.quit()
def open_settings():
    menu_parent.enabled = False
    settings_menu.enabled = True
def back_to_menu():
    settings_menu.enabled = False
    menu_parent.enabled = True

def LoadMainMenu():
    Text("Celestial Combat", parent=menu_parent, scale=35, y=3.5, x=-3.75, font='Bitcountprop.ttf')
    Text("V1.1", parent=menu_parent, scale=30, y=2.5, x=-0.75, font='Bitcountprop.ttf')
    Button(text='Start', scale=(2.5, 1), y=1, parent=menu_parent, on_click=start_game)
    Button(text='Settings', scale=(2.5, 1), y=-0.5, parent=menu_parent, on_click=open_settings)
    Button(text='Quit', scale=(2.5, 1), y=-2, parent=menu_parent, on_click=quit_game)

def LoadSettingsMenu():
    global volume_slider
    Text("Settings", parent=settings_menu, scale=35, y=2, x=-2, font='Bitcountprop.ttf')
    volume_slider = Slider(scale=20, min=0, max=1, default=0.5, step=0.1, y=0.1, x=-1, parent=settings_menu)
    def on_volume_change(): 
        if current_music: current_music.volume = volume_slider.value
    volume_slider.on_value_changed = on_volume_change
    Text("Volume", parent=settings_menu, y=-0.5, scale=10, x=-0.5, font='Bitcountprop.ttf')
    Button(text='Back', scale=(2.5, 1), y=-2, parent=settings_menu, on_click=back_to_menu)

def update():
    global fight_active, fireball_damage, speed

    if held_keys['shift']:
        speed *= 2 

    if menu_parent.enabled:
        return

    update_traders(1.5, 1)

    fireball_damage = 25 + (5 * better_fireball_counter)

    for trader in wandering_traders:
        if player.intersects(trader).hit:
            start_fight(trader)
            break


    if player.enabled and not fight_active:
        x = int(held_keys['d']) - int(held_keys['a'])
        y = int(held_keys['w']) - int(held_keys['s'])
        move = Vec2(x, y)

        speed = playerspeed
        for grass in grass_entities:
            if player.intersects(grass).hit:
                speed *= 0.6
                break

        if move.length() > 0:
            move = move.normalized() * speed * time.dt
            player.position += Vec3(move.x, move.y, 0)
            player.rotation_z = lerp(player.rotation_z, x * 10, time.dt * 10)
        else:
            player.rotation_z = lerp(player.rotation_z, 0, time.dt * 10)

        camera.position = lerp(camera.position, (player.x, player.y, -10), time.dt * 5)
        background2.position = (camera.x, camera.y, background2.z)

background2 = Entity(model='quad', z=1, scale=(50, 30), color=color.hex("#615F3C"), enabled=False)
background = Panel(parent=menu_parent, scale=999, color=color.hex('#218eb4'), z=1)

LoadMainMenu()
LoadSettingsMenu()
play_next_song()

window.title = 'Celestial-Combat V1.1'
window.fullscreen = False
app.run()
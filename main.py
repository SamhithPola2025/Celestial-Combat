from ursina import *
import random, math, time

app = Ursina()

camera.orthographic = True
camera.fov = 10

menu_parent = Entity()
settings_menu = Entity(enabled=False)
grass_entities = []
fight_window = Entity(parent=camera.ui, enabled=False, z=10)
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
    scale=(6, 3),
    color=color.hex("#333333aa")  # Semi-transparent dark background
)

# Fix the attack options dialogue positioning
attackoptionsdialogue.position = (0, -0.2)  # Center it vertically, slightly below center
attackoptionsdialogue.z = -1  # Make sure it's above the background but below text

attack1button = Button(
    parent=attackoptionsdialogue,
    enabled=False,
    scale=(2, 1),
    color=color.hex("#b1a022"),
    text='Skip turn',
    font='Bitcountprop.ttf'
)

attack2button = Button(
    parent=attackoptionsdialogue,
    enabled=False,
    scale=(2, 1),
    color=color.hex('#b1a022'),
    text='Fire ball',
    font='Bitcountprop.ttf'
)

attack3button = Button(
    parent=attackoptionsdialogue,
    enabled=False,
    scale=(2, 1),
    color=color.hex('#b1a022'),
    text='Push',
    font='Bitcountprop.ttf'
)

# Position the attack buttons within the dialogue
attack1button.position = (-1.2, 0.4)
attack2button.position = (0, 0.4)
attack3button.position = (1.2, 0.4)
attack1button.z = attack2button.z = attack3button.z = -2  # Ensure buttons are above the panel

attack_button = Button(
    text='Attack',
    parent=fight_window,
    y=-0.1,
    x=-0.6,
    scale=(0.8,0.8),
    color=color.azure,
    highlight_color=color.light_gray,
    pressed_color=color.blue,
)

run_button = Button(
    text='Run',
    parent=fight_window,
    y=-0.1,
    x=0.6,
    scale=(0.8,0.8),
    color=color.red,
    highlight_color=color.light_gray,
    pressed_color=color.blue,
)

fight_window.z = 100
fight_text.z = 0.1
attack_button.z = 0.1
run_button.z = 0.1

wandering_trader = Entity(model='quad', texture='sprites/enemy', scale=(0.8, 0.9),
                          position=(3,3,1), collider='box', enabled=False)

player = Entity(model='quad', texture='sprites/player', scale=(0.8, 1), y=1,
                collider='box', enabled=False)

playerspeed = 5
player_health = 100
enemy_health = 100
fight_active = False
player_turn = True  # turn-based flag

# player health display
player_health_text = Text(
    f"Player HP: {player_health}",
    origin=(0.5, -0.5),
    position=(-0.8, 0.45),
    scale=2,
    font='Bitcountprop.ttf'
)

# ----- fight logic -----
def start_fight():
    global fight_active, player_turn, player_health, enemy_health
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

def end_fight():
    global fight_active
    fight_active = False
    fight_window.enabled = False
    player.enabled = True
    attackoptionsdialogue.enabled = False
    top_wins_counter.enabled = True
    top_wins_counter.text = f"Wins: {wins}"

def attack_player_move(attack_type):
    global enemy_health, player_turn
    if not player_turn:
        return

    if attack_type == "skip":
        print("Player skipped turn")
    elif attack_type == "fire":
        enemy_health -= 25
    elif attack_type == "push":
        enemy_health -= 10

    fight_text.text = f"Enemy health: {max(enemy_health,0)}"
    attackoptionsdialogue.enabled = False

    if enemy_health <= 0:
        fight_text.text = "You Win!"
        global wins
        wins += 1
        print(f"wins: {wins}, wins updated")
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

# connect attack buttons
attack1button.on_click = lambda: attack_player_move("skip")
attack2button.on_click = lambda: attack_player_move("fire")
attack3button.on_click = lambda: attack_player_move("push")

# attack button now shows attack options only on player's turn
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

# ----- music -----
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

# ----- grass generation -----
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

# ----- trader logic -----
def tradercode(move_distance=3, speed=2):
    wandering_trader.position = (player.x, player.y + 2, 0)
    wandering_trader.base_x = player.x
    wandering_trader.base_y = player.y + 2

    def trader_update():
        t = time.time() * speed
        offset = math.sin(t) * move_distance
        wandering_trader.x = wandering_trader.base_x + offset
        wandering_trader.y = wandering_trader.base_y
    wandering_trader.update = trader_update

# ----- game start -----
def start_game():
    menu_parent.enabled = False
    player.enabled = True
    wandering_trader.enabled = True
    camera.position = (player.x, player.y, -10)
    background2.enabled = True
    background.enabled = False
    grassgen(150, 12)
    tradercode()
    fight_window.enabled = False
    top_wins_counter.enabled = True

def quit_game(): application.quit()
def open_settings():
    menu_parent.enabled = False
    settings_menu.enabled = True
def back_to_menu():
    settings_menu.enabled = False
    menu_parent.enabled = True

# ----- menus -----
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

# ----- main update -----
def update():
    global fight_active
    if menu_parent.enabled:
        return

    if player.enabled and wandering_trader.enabled and not fight_active:
        if player.intersects(wandering_trader).hit:
            start_fight()

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

# ----- backgrounds -----
background2 = Entity(model='quad', z=-100, scale=(50, 30), color=color.hex("#615F3C"), enabled=False)
background = Panel(parent=menu_parent, scale=999, color=color.hex('#218eb4'), z=1)

# ----- init -----
LoadMainMenu()
LoadSettingsMenu()
play_next_song()

window.title = 'Celestial-Combat V1.1'
window.fullscreen = False
app.run()
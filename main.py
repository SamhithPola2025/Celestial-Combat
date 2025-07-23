from ursina import *

app = Ursina()

# Set up camera
camera.orthographic = True
camera.fov = 10  # Field of view for orthographic camera

# Create menus
menu_parent = Entity()
settings_menu = Entity(enabled=False)

# Game entities
grassinstance = Entity(model='quad', color=color.green, scale=(20, 20), y=-0.25, enabled=False)
player = Entity(model='quad', color=color.orange, scale=0.5, y=1, enabled=False)

playerspeed = 5

# Background
background = Panel(
    parent=menu_parent,
    scale=999,
    color=color.hex('#218eb4'),
    z=1  
)

# Music system
music_files = [
    r'music/ready-set-drift-michael-grubb-main-version-24555-02-59.mp3',
    r'music/space-ranger-moire-main-version-03-04-10814.mp3',
    r'music/easy-arcade-hartzmann-main-version-28392-02-32.mp3'
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

def start_game():
    menu_parent.enabled = False
    player.enabled = True
    grassinstance.enabled = True
    # Set initial camera position
    camera.position = (player.x, player.y, -10)

def quit_game():
    application.quit()

def open_settings():
    menu_parent.enabled = False
    settings_menu.enabled = True

def back_to_menu():
    settings_menu.enabled = False
    menu_parent.enabled = True

def LoadMainMenu():
    Text("Celestial Combat", parent=menu_parent, scale=3.5, y=3.5, x=-3.75, z=0, font='Bitcountprop.ttf')
    Text("V1.1", parent=menu_parent, scale=3, y=2.5, x=-0.75, z=0, font='Bitcountprop.ttf')

    start_btn = Button(text='Start', scale=(2.5, 1), y=1, parent=menu_parent, on_click=start_game)
    start_btn.text_entity.font = 'Bitcountprop.ttf'

    settings_btn = Button(text='Settings', scale=(2.5, 1), y=-0.5, parent=menu_parent, on_click=open_settings)
    settings_btn.text_entity.font = 'Bitcountprop.ttf'

    quit_btn = Button(text='Quit', scale=(2.5, 1), y=-2, parent=menu_parent, on_click=quit_game)
    quit_btn.text_entity.font = 'Bitcountprop.ttf'

def LoadSettingsMenu():
    global volume_slider, current_music

    Text("Settings", parent=settings_menu, scale=2, y=0.3, z=0, font='Bitcountprop.ttf')

    volume_slider = Slider(scale=4, min=0, max=1, default=0.5, step=0.01, y=0.1, parent=settings_menu)

    def on_volume_change():
        if current_music:
            current_music.volume = volume_slider.value

    volume_slider.on_value_changed = on_volume_change

    Text("Volume", parent=settings_menu, y=0.2, scale=1, z=0, font='Bitcountprop.ttf')

    back_btn = Button(text='Back', scale=(0.3, 0.1), y=-0.3, parent=settings_menu, on_click=back_to_menu)
    back_btn.text_entity.font = 'Bitcountprop.ttf'

def update():
    # Player movement
    if player.enabled:
        x = held_keys['d'] - held_keys['a']
        y = held_keys['w'] - held_keys['s']
        move = Vec2(x, y)
        
        if move.length() > 0:
            move = move.normalized() * playerspeed * time.dt
            player.position += Vec3(move.x, move.y, 0)
        
        # Camera follows player with smooth transition
        camera.position = lerp(camera.position, (player.x, player.y, -10), time.dt * 5)

# Initialize menus
LoadMainMenu()
LoadSettingsMenu()

# Start music
play_next_song()

# Window settings
window.title = 'Celestial-Combat V1.1'
window.borderless = False
window.fullscreen = False

app.run()
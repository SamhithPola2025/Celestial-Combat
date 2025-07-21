from ursina import *

app = Ursina()

menu_parent = Entity()
settings_menu = Entity(enabled=False)

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

music_index = 0
current_music = None
volume_slider = None  # initialize here for scope clarity

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
    print('starting game')
    menu_parent.enabled = False

def quit_game():
    application.quit()

def open_settings():
    menu_parent.enabled = False
    settings_menu.enabled = True

def back_to_menu():
    settings_menu.enabled = False
    menu_parent.enabled = True

def LoadMainMenu():
    Text("Main Menu", parent=menu_parent, scale=2, y=0.3, z=0)

    Button(text='Start', scale=(2, 1), y=1.5, parent=menu_parent, on_click=start_game)
    Button(text='Settings', scale=(2, 1), y=0, parent=menu_parent, on_click=open_settings)
    Button(text='Quit', scale=(2, 1), y=-1.5, parent=menu_parent, on_click=quit_game)

def LoadSettingsMenu():
    global volume_slider

    Text("Settings", parent=settings_menu, scale=2, y=0.3, z=0)

    volume_slider = Slider(min=0, max=1, default=0.5, step=0.01, y=0.1, parent=settings_menu)
    
    def on_volume_change():
        if current_music:
            current_music.volume = volume_slider.value
    
    volume_slider.on_value_changed = on_volume_change

    Text("Volume", parent=settings_menu, y=0.2, scale=1, z=0)

    Button(text='Back', scale=(0.3, 0.1), y=-0.3, parent=settings_menu, on_click=back_to_menu)

LoadMainMenu()
LoadSettingsMenu()

play_next_song()

window.title = 'Celestial-Combat V1.1'

app.run()

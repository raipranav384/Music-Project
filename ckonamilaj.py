from pypiano import Piano
# from pynput import keyboard

carnatic_to_western = {
    'S': 'C',
    'r': 'C#',
    'R': 'D',
    'g': 'D#',
    'G': 'E',
    'M': 'F',
    'm': 'F#',
    'P': 'G',
    'd': 'G#',
    'D': 'A',
    'n': 'A#',
    'N': 'B'
}

p = Piano()

def play_swaras(swaras):
    for swara in swaras:
        if swara in carnatic_to_western:
            p.play(carnatic_to_western[swara])
            p.pause(0.5)

def on_press(key):
    try:
        play_swaras(key.char)
    except AttributeError:
        pass

for key in carnatic_to_western:
    play_swaras(key)
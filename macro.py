from time import sleep
import pyautogui
import pyKey
from pyKey import key_dict

pyauto_keys = [(repr(key).lstrip("'").rstrip("'")) if key != "'" else repr(key).lstrip('"').rstrip('"') for key in pyautogui.KEYBOARD_KEYS if key != ' ']
pykeys = [key for key in key_dict.win_keys.keys()]

# MOVE TO
def move_to_settings(full_string):
    initial_values = full_string.replace('Mouse move to (','').replace(')','')
    prompt = 'Type the coordinates in the format "X,Y"'
    error = 'Error: You have to type in an integer, no decimals!'
    return {'Prompt':prompt, 'InitialValue': initial_values, 'Error': error}

def edit_move_to(coordinates):
    formatted = coordinates.replace(' ', '').split(',')

    if len(formatted) != 2:
        return False
    try:
        x = formatted[0]
        y = formatted[1]
        int(x)
        int(y)
        return f"Mouse move to ({x},{y})"
    except ValueError:
        return False

def move_to(string):
    start: str = string.split('(')[1]
    x = start.split(',')[0]
    y = start.split(',')[1].replace(')','')
    pyautogui.moveTo(int(x),int(y),1)

# WRITE
def write_settings(full_string: str):
    text = full_string[7:-1]
    return {'Prompt': 'Type the text the command will write.', 'InitialValue': text}

def edit_write(string):
    return f"Write ({string})"

def write(full_string):
    text = full_string[7:-1]
    pyautogui.write(text, 0.12)

#PRESS
def press_settings(full_string):
    return {'Prompt': 'Choose which button to press.', 'Values':pyauto_keys, 'Wrap':18, 'Direction': 'horizontal'}

def edit_press(string):
    return f"Press ({string})"

def press(full_string):
    text = full_string[7:-1]
    pyautogui.press(text)

#WAIT
def wait_settings(full_string):
    text = full_string[6:-1]
    return {'Prompt': 'Type the amount of seconds to wait.', 'InitialValue': text, 'Error': 'Error: You have to type a number, no letters or symbols!'}

def edit_wait(string):
    try:
        float(string)
        return f'Wait ({string})'
    except ValueError:
        return False

def wait(full_string):
    text = full_string[6:-1]
    sleep(float(text))

# KEYDOWN
def keydown_settings(full_string):
    return {'Prompt': 'Choose which button to press.', 'Values':pykeys, 'Wrap':18, 'Direction': 'horizontal'}

def edit_keydown(string):
    return f"Keydown ({string})"

def keydown(full_string):
    text = full_string[9:-1]
    pyKey.pressKey(text)
    #keyboard.press_key(text if len(text) == 1 else keyboard.__getattribute__(text))
    #pyautogui.keyDown(text)

# KEYUP
def keyup_settings(full_string):
    return {'Prompt': 'Choose which button to press.', 'Values':pykeys, 'Wrap':18, 'Direction': 'horizontal'}

def edit_keyup(string):
    return f"Keyup ({string})"

def keyup(full_string):
    text = full_string[7:-1]
    pyKey.releaseKey(text)
    #keyboard.release_key(text if len(text) == 1 else keyboard.__getattribute__(text))
    # pyautogui.keyUp(text)

# Mouse1 Down

# Mouse1 Up

# Mouse2 Down

# Mouse2 Up

# -- EVERYTHING ELSE --
everything = {
    'Mouse move to ': {'OptionText': 'Mouse move to (x,y)', 'DefaultValue': 'Mouse move to (500,500)', 'Settings': move_to_settings, 'Edit': edit_move_to, 'Command': move_to},
    'Left Click': {'Command': pyautogui.click},
    'Right Click': {'Command': pyautogui.rightClick},
    'Write ': {'OptionText': 'Write (text)', 'DefaultValue': 'Write (Hello World!)', 'Settings': write_settings, 'Edit':edit_write, 'Command': write},
    'Press ': {'OptionText': 'Press (button)', 'DefaultValue': 'Press (enter)', 'Settings': press_settings, 'Edit': edit_press, 'Command': press},
    'Wait ': {'OptionText': 'Wait (seconds)', 'DefaultValue': 'Wait (1)', 'Settings': wait_settings, 'Edit': edit_wait, 'Command': wait},
    'Keydown ': {'OptionText': 'Keydown (button)', 'DefaultValue': 'Keydown (SPACEBAR)', 'Settings': keydown_settings, 'Edit': edit_keydown, 'Command': keydown},
    'Keyup ': {'OptionText': 'Keyup (button)', 'DefaultValue': 'Keyup (SPACEBAR)', 'Settings': keyup_settings, 'Edit': edit_keyup, 'Command': keyup},
    'Mouse1 Down': {'Command': lambda: pyautogui.mouseDown(button='left')},
    'Mouse1 Up': {'Command': lambda: pyautogui.mouseUp(button='left')},
    'Mouse2 Down': {'Command': lambda: pyautogui.mouseDown(button='right')},
    'Mouse2 Up': {'Command': lambda: pyautogui.mouseUp(button='right')}
}

def follow_command(command:str):
    text = command.split('(')[0]
    try:
        everything[text]['Command']()
    except TypeError:
        everything[text]['Command'](command)
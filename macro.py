import pyautogui
keys = [r'\t', r'\n', r'\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
'8', '9', ':', ';', '<', '=', '>', '?', '@', '[', r'\\', ']', '^', '_', '`',
'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
'browserback', 'browserfavorites', 'browserforward', 'browserhome',
'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
'command', 'option', 'optionleft', 'optionright']

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
    return {'Prompt': 'Choose which button to press.', 'Values':keys, 'Wrap':19, 'Direction': 'horizontal'}

def edit_press(string):
    return f"Press ({string})"

def press(full_string):
    text = full_string[7:-1]
    pyautogui.press(text)

# -- EVERYTHING ELSE --
everything = {
    'Mouse move to ': {'OptionText': 'Mouse move to (x,y)', 'DefaultValue': 'Mouse move to (500,500)', 'Settings': move_to_settings, 'Edit': edit_move_to, 'Command': move_to},
    'Left Click': {'Command': pyautogui.click},
    'Right Click': {'Command': pyautogui.rightClick},
    'Write ': {'OptionText': 'Write (text)', 'DefaultValue': 'Write (Hello World!)', 'Settings': write_settings, 'Edit':edit_write, 'Command': write},
    'Press ': {'OptionText': 'Press (button)', 'DefaultValue': 'Press (enter)', 'Settings': press_settings, 'Edit': edit_press, 'Command': press},
}

def follow_command(command:str):
    text = command.split('(')[0]
    try:
        everything[text]['Command']()
    except TypeError:
        everything[text]['Command'](command)
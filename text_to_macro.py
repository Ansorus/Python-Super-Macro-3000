import pyautogui

def move_to(string):
    start: str = string.split('(')[1]
    x = start.split(',')[0]
    y = start.split(',')[1].replace(')','')
    pyautogui.moveTo(int(x),int(y))

text_to_command = {
    "Left Click":pyautogui.click,
    "Right Click": pyautogui.rightClick,
    "Mouse move to ": move_to,
}

def follow_command(command:str):
    text = command.split('(')[0]

    try:
        text_to_command[text]()
    except TypeError:
        text_to_command[text](command)
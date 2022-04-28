import pyautogui
import time
import pytesseract
from pynput.mouse import Listener
from PIL import ImageGrab
from pynput.keyboard import Key, Controller


keyboard = Controller()
values = []


def on_click(x, y, button, pressed):
    if pressed:
        x, y = get_xy_values()
        values.append(x)
        values.append(y)

        if len(values) > 2:
            time.sleep(1)

            screenshot(values)
            typing("text.png")


def convert_pos_to_str(xy_val):
    x_val = xy_val[xy_val.find("=") + 1: xy_val.find(",")]
    y_val = xy_val[xy_val.find("y") + 2: -1]

    return x_val, y_val


def get_xy_values():
    xy_val = str(pyautogui.position())

    x, y = convert_pos_to_str(xy_val)

    return int(x), int(y)


def screenshot(values):
    x1, y1 = values[0], values[1]
    x2, y2 = values[2], values[3]

    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

    screenshot.save("text.png")


def typing(img):
    text = pytesseract.image_to_string(img)
    time.sleep(3)

    for i in text:
        if i == "|":
            time.sleep(0.007)
            keyboard.type("I")

        elif i == "\n":
            time.sleep(0.007)
            keyboard.type(" ")

        else:
            time.sleep(0.007)
            keyboard.type(i)


with Listener(on_click=on_click) as listener:
    listener.join()

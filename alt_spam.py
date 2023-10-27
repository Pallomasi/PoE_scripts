import pyautogui,random,time, bezier, win32api, pytesseract, mss
import numpy as np
from PIL import Image

# Disable pyautogui pauses
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0

#init tesseract exec
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def init_positions(mode):
    location = "screenshot"
    if mode == "simulator":
        location = location+"_"+mode
    alt_loc = pyautogui.locateCenterOnScreen(location + "/alt.png")
    aug_loc = pyautogui.locateCenterOnScreen(location + "/aug.png")
    itm_loc = pyautogui.locateCenterOnScreen(location + "/itm.png")
    if mode == "simulator":
        itm_with_offset = (itm_loc.x + 0, itm_loc.y - 100)
    else:
        itm_with_offset = (itm_loc.x + 100, itm_loc.y + 0)
    return (alt_loc,aug_loc,itm_with_offset)

#Returns whether the given key is currently pressed down
def isKeyPressed(key):
    #"if the high-order bit is 1, the key is down; otherwise, it is up."
    return (win32api.GetKeyState(key) & (1 << 7)) != 0

#Returns whether the given key is currently toggled on. kay no. 20 is caps lock
def isKeyToggled(key):
    return (win32api.GetKeyState(key) & 0xffff) != 0

def small_delay():
    time.sleep(random.randint(100,125)/1000)

def create_control(start,end,rand):
    control = [(abs(start[0]-end[0])*rand), (abs(start[1]-end[1])*rand)]
    control[0] = round(control[0])+min(start[0],end[0]+random.randint(-300,300))
    control[1] = round(control[1])+min(start[1],end[1]+random.randint(-300,300))
    return tuple(control)

def mouse_transition(loc):
    delay = random.randint(100,150)/1000
    start = pyautogui.position()
    control1 = create_control(start,loc,random.randint(30,40)/100)
    control2 = create_control(start,loc,random.randint(60,70)/100)

    control_points = np.array([start, control1, control2, loc])
    points = np.array([control_points[:,0], control_points[:,1]])

    degree = 3
    curve = bezier.Curve(points, degree)
    curve_steps = 50
    delay = 1/curve_steps
    for i in range(1, curve_steps+1):
        x, y = curve.evaluate(i/curve_steps)
        pyautogui.moveTo(x, y)
        pyautogui.sleep(delay)

def explicit_room_check():
    with mss.mss() as sct:
        monitor = {"top": 547, "left": 40, "width": 400, "height": 100}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        img = np.array(sct.grab(monitor))
        mods = (pytesseract.image_to_string(img, config='tessedit_char_whitelist=0123456789'))
    if "PREFIX MODIFIER" in mods and "SUFFIX MODIFIER" in mods:
        return False
    else:
        return True

def check_if_done(good_mod):
    with mss.mss() as sct:
        monitor = {"top": 547, "left": 40, "width": 400, "height": 100}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        img = np.array(sct.grab(monitor))
        mods = (pytesseract.image_to_string(img, config='tessedit_char_whitelist=0123456789'))
    if good_mod in mods:
        return True
    else:
        return False

def crafting_loop(alt_loc,aug_loc,itm_loc,good_mod):
    done = False
    while not done:
        mouse_transition(alt_loc)
        pyautogui.click()
        #pyautogui.click(button='right')
        small_delay()
        mouse_transition(itm_loc)
        pyautogui.click()
        small_delay()
        if explicit_room_check():
            mouse_transition(aug_loc)
            pyautogui.click()
            #pyautogui.click(button='right')
            small_delay()
            mouse_transition(itm_loc)
            pyautogui.click()
            small_delay()
        if check_if_done(good_mod):
            break
        if isKeyToggled(20):
            break

if __name__ == '__main__':

    good_mod = "FIRE DAMAGE TO ATTACKS"
    alt_loc,aug_loc,itm_loc = init_positions("simulator")
    crafting_loop(alt_loc,aug_loc,itm_loc,good_mod)

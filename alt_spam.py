import pyautogui,random,time
import win32api

def init_positions(mode):
    location = "screenshot"
    if mode == "simulator":
        location = location+"_"+mode
    alt_loc = pyautogui.locateCenterOnScreen(location + "/alt.png")
    aug_loc = pyautogui.locateCenterOnScreen(location + "/aug.png")
    itm_loc = pyautogui.locateCenterOnScreen(location + "/itm.png")
    itm_with_offset = (itm_loc.x + 100, itm_loc.y + 0)
    return (alt_loc,aug_loc,itm_with_offset)

#Returns whether the given key is currently pressed down
def isKeyPressed(key):
    #"if the high-order bit is 1, the key is down; otherwise, it is up."
    return (win32api.GetKeyState(key) & (1 << 7)) != 0

#Returns whether the given key, such as caps lock, is currently toggled on
def isKeyToggled(key):
    return (win32api.GetKeyState(key) & 0xffff) != 0

def small_delay():
    time.sleep(random.randint(100,125)/1000)

def item_click(loc):
    pyautogui.moveTo(loc)

def check_if_done():
    location_button = pyautogui.locateOnScreen("screenshot/complete.png")
    if location_button:
        return True

def crafting_loop(alt_loc,aug_loc,itm_loc):
    done = False
    while not done:
        item_click(alt_loc)
        pyautogui.click(button='right')
        small_delay()
        item_click(itm_loc)
        pyautogui.click()
        small_delay()
        item_click(aug_loc)
        pyautogui.click(button='right')
        small_delay()
        item_click(itm_loc)
        pyautogui.click()
        small_delay()
        done = check_if_done()
        if isKeyToggled(20):
            break

if __name__ == '__main__':

    alt_loc,aug_loc,itm_loc = init_positions("simulator")
    print (alt_loc,aug_loc,itm_loc)
    #crafting_loop(alt_loc,aug_loc,itm_loc)
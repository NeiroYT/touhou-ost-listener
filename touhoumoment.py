from random import randint
import time
import keyboard
import undetected_chromedriver as wd
from multiprocessing import Process

sleep_mode = 1 # sleep fully or not
working_mode = 1 # start randomly or not
repet_mode = 1 # repeat used tracks or not
chrome_path = r""
hotkey_pressed = False

def on_hotkey_press():
    global hotkey_pressed
    hotkey_pressed = True

def controllable_sleep(secs):
    global hotkey_pressed
    process = Process(target=time.sleep, args=(secs,))
    process.start()
    keyboard.add_hotkey("ctrl+alt+q", on_hotkey_press)
    while (not hotkey_pressed and process.is_alive()):
        time.sleep(1)
    keyboard.clear_all_hotkeys()
    hotkey_pressed = False
    process.terminate()

def save_list(list_urls, list_timings):
    with open("checkpoint", 'w+') as file:
        file.write(str(len(list_urls)))
        file.write('\n')
        for line in list_urls:
            file.write(line)
            file.write('\n')
        for line in list_timings:
            file.write(str(line))
            file.write('\n')

def load_list():
    list1 = open_file('checkpoint')
    listlen = int(list1[0])
    list_url = []
    list_timings = []
    for i in range(1, listlen+1):
        list_url.append(list1[i])
    for i in range(listlen+1, len(list1)):
        list_timings.append(int(list1[i]))
    return list_url, list_timings


def opener(link, timed=0, dur=0):
    if working_mode == 0:
        browser.get(link)
        return 0
    elif working_mode == 1:
        if (dur-timed) > 0:
            rngmove = randint(0, dur-timed)
        else:
            rngmove = 0
        browser.get(f'{link}&t={rngmove}s')
        return rngmove
# returns where it starts

def convert_time(list2):
    newlist = []
    for item in list2:
        newlist.append(item.split(':'))
    for timings in enumerate(newlist):
        newlist[timings[0]] = (int(timings[1][0])*60)+int(timings[1][1]) # MM:SS to secs
    return newlist
# MM:SS (from excel) to N seconds

def NumsInit():
    list1 = open_file("currentbaseNums.ini")
    for item in enumerate(list1):
        list1[item[0]] = list1[item[0]].split(' ', 1)
        list1[item[0]][0] = list(map(int, list1[item[0]][0].split('-', 1))) # ["num-num", "name"] to [[num, num], "name"]
    return list1
# [[num, num], "name"]

def Global_Asker():
    global sleep_mode, working_mode, repet_mode, chrome_path
    try:
        try:
            chrome_path = open_file('chrome_path')[0]
        except:
            chrome_path = input('Chrome executable path: ')
            with open('chrome_path', 'w+') as file:
                file.write(chrome_path)
                file.write('\n')
        sleep_mode = int(input('0 - play full track, 1 - play N seconds of track, 2 - play N seconds with console wait after each: '))
        working_mode = int(input('0 - play from the start, 1 - play from random second: '))
        repet_mode = int(input('0 - play with no repeats in tracklist, 1 - allow repeats: '))
    except ValueError:
        print('Error, so changed to 0, 0, 1.')
        sleep_mode = 0
        working_mode = 0
        repet_mode = 1
    if sleep_mode < 0 or sleep_mode > 2:
        sleep_mode = 0
    if working_mode < 0 or working_mode > 1:
        working_mode = 0
    if repet_mode < 0 or repet_mode > 1:
        repet_mode = 1

## Lazy convertion of my Excel output (youtube playlist -> txt file)
## Check example in "base" before inserting your own URLs
## pairs of urls from playlist in base.txt -> single urls without playlist and indexes
def convert_playlist_urls():
    list_url = []
    with open("base", 'r') as file:
        list_url = file.readlines()
    for item in enumerate(list_url):
        list_url[item[0]] = item[1].split('&') # "https://...&...&..." -> [url, playlist, index]
    list_t = []
    for index1 in range(0, len(list_url), 2):
        list_t.append(list_url[index1][0])
    print(list_t)
    with open("temp_urls", 'w+') as file2:
        for line in list_t:
            file2.write(line)
            file2.write('\n')
    print('success')
## data in temp_urls can be inserted in a current_urls file

def open_file(name):
    with open(name, 'r') as file:
        list1 = file.readlines()
    for item in enumerate(list1):
        list1[item[0]] = item[1][:-1:]
    return list1

if __name__ == '__main__':
    numsBase = NumsInit()
    #print(numsBase)
    #convert_playlist_urls()
    load = True
    try:
        checkpoint = open_file("checkpoint")
    except Exception as e:
        load = False
    if (load):
        try:
            answ = int(input("Load previous tracks? (0 - yes, 1 - NO): "))
            if (answ == 1):
                load = False
        except ValueError:
            print("Tracks weren't loaded.")
            load = False
    if (load):
        list_url, list_t = load_list()

    Global_Asker()
    suggested_time = 0
    if sleep_mode == 1 or sleep_mode == 2:
        try:
            suggested_time = int(input('Amount of seconds for each track (minimum 1): '))
        except ValueError:
            print('Changed to 10')
            suggested_time = 10
        if suggested_time < 1:
            suggested_time = 10
    try:
        browser = wd.Chrome(driver_executable_path='chromedriver.exe', browser_executable_path=chrome_path) # Start Compatible version of chromedriver.exe
    except Exception as e:
        file = open('chrome_path', 'w+')
        file.close()
        raise e
    r = 0
    if (not load):
        list_url = open_file("current_urls") # list_url - URLs, list_t - lengths
        list_t = open_file("current_timings") # Amount of durations should be the same with the amount of urls
        list_t = convert_time(list_t)
        SwitchList = open_file("SWITCHERS.ini") # switchers
        for item in enumerate(SwitchList):
            if item[1][0] == '0':
                startN = numsBase[item[0]][0][0] # get startindex
                if len(numsBase[item[0]][0]) == 2: # if end exists, use it for endN
                    endN = numsBase[item[0]][0][1]
                else:
                    endN = startN
                numsBase[item[0]] = 0 # discarded game
                for song in range(startN-1, endN): # tracks destroyer... be careful
                    list_url.pop(startN-1)
                    list_t.pop(startN-1)
                for elemindex in range(item[0]+1, len(numsBase)):
                    numsBase[elemindex][0][0] -= endN-startN+1 # all next starts get subtracted
                    if len(numsBase[elemindex][0]) == 2:
                        numsBase[elemindex][0][1] -= endN-startN+1 # same for ends
    while 1:
        if r != '1':
            randnum = randint(1, len(list_url))
        print(f'\nOpened URL #(hidden): {list_url[randnum-1]} (video with (hidden)s length) Press Ctrl+Alt+Q to skip') # no cheats for prompt viewer
        #print(f'\nOpened URL #{randnum}: {list_url[randnum-1]} (video with {list_t[randnum-1]}s length) Press Ctrl+Alt+Q to skip')
        rng = opener(list_url[randnum-1], suggested_time, list_t[randnum-1])
        if sleep_mode == 0:
            controllable_sleep(list_t[randnum-1]-rng+4)
        elif sleep_mode == 1:
            controllable_sleep(suggested_time)
        elif sleep_mode == 2:
            controllable_sleep(suggested_time)
            browser.get('about:blank')
            r = input('\n\n1 - repeat again, something else - continue with new track\n\n')
        if r != '1':
            if repet_mode == 0:
                list_url.pop(randnum-1)
                list_t.pop(randnum-1)
                save_list(list_url, list_t)
        if len(list_url) == 0 or len(list_t) == 0:
            print("No tracks left...\n")
            break

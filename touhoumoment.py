from random import randint
import time
import selenium.webdriver as wd

sleep_mode = 1 # sleep fully or not
working_mode = 1 # start randomly or not
repet_mode = 1 # repeat used tracks or not

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
    global sleep_mode, working_mode, repet_mode
    try:
        sleep_mode = int(input('0 - play full track, 1 - play N seconds, 2 - play N seconds with console wait: '))
        working_mode = int(input('0 - play from the start, 1 - play from random second: '))
        repet_mode = int(input('0 - play with no repeats in tracklist, 1 - allow repeats: '))
    except ValueError:
        print('Changed to 0, 0, 1.')
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
    list1 = []
    with open("base", 'r') as file:
        list1 = file.readlines()
    for item in enumerate(list1):
        list1[item[0]] = item[1].split('&') # "https://...&...&..." -> [url, playlist, index]
    list2 = []
    for index1 in range(0, len(list1), 2):
        list2.append(list1[index1][0])
    print(list2)
    with open("temp_urls", 'w+') as file2:
        for line in list2:
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
    Global_Asker()
    suggested_time = 0
    if sleep_mode == 1 or sleep_mode == 2:
        try:
            suggested_time = int(input('Seconds cooldown (minimum 1): '))
        except ValueError:
            print('Changed to 10')
            suggested_time = 10
        if suggested_time < 1:
            suggested_time = 10
    browser = wd.Chrome('chromedriver.exe') # Start Compatible version of chromedriver.exe
    r = 0
    list1 = open_file("current_urls") # list1 - URLs, list2 - lengths
    list2 = open_file("current_timings") # Amount of durations should be the same with the amount of urls
    SwitchList = open_file("SWITCHERS.ini") # switchers
    list2 = convert_time(list2)
    for item in enumerate(SwitchList):
        if item[1][0] == '0':
            startN = numsBase[item[0]][0][0] # get startindex
            if len(numsBase[item[0]][0]) == 2: # if end exists, use it for endN
                endN = numsBase[item[0]][0][1]
            else:
                endN = startN
            numsBase[item[0]] = 0 # discarded game
            for song in range(startN-1, endN): # tracks destroyer... be careful
                list1.pop(startN-1)
                list2.pop(startN-1)
            for elemindex in range(item[0]+1, len(numsBase)):
                numsBase[elemindex][0][0] -= endN-startN+1 # all next starts get subtracted
                if len(numsBase[elemindex][0]) == 2:
                    numsBase[elemindex][0][1] -= endN-startN+1 # same for ends
    while 1:
        if r != '1':
            randnum = randint(1, len(list1))
        print(f'\nOpened URL #(hidden): {list1[randnum-1]} (video with (hidden)s length)\n') # no cheats for prompt viewer
        #print(f'\nOpened URL #{randnum}: {list1[randnum-1]} (video with {list2[randnum-1]}s length)\n')
        rng = opener(list1[randnum-1], suggested_time, list2[randnum-1])
        if sleep_mode == 0:
            time.sleep(list2[randnum-1]-rng+4)
        elif sleep_mode == 1:
            time.sleep(suggested_time)
        elif sleep_mode == 2:
            time.sleep(suggested_time)
            browser.get('about:blank')
            r = input('\n\nWaiting for something to happen?\n\n')
        if r != '1':
            if repet_mode == 0:
                list1.pop(randnum-1)
                list2.pop(randnum-1)
        if len(list1) == 0 or len(list2) == 0:
            print("No tracks left...\n")
            break

# This is a very naive interface...
# You can modify the handler and add more stuffs, like sending text messages.
# Good luck!

import winsound
import requests
import threading
import time

# Frequency
interval = 5

# GRE-Website
url = 'http://gre-main.neea.cn/html1/category/1507/1795-1.htm'
lib = [] # ["a href='/html1/report/20053/670-1.htm' target='_self' title=\"关于取消2020年6月GRE考试的通知\""]
# tmplib = []


def beep():
    t = threading.current_thread()
    while getattr(t, "do_run", True):
        for i in range(600, 800, 100):
            winsound.Beep(i, 1000)


def get_date_string():
    time_string = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time_string


def parse_title(text, cursor, n):
    counter = 0
    pos0, pos1 = cursor, cursor
    while True:
        if text[cursor] == '<':
            pos0 = cursor
        elif text[cursor] == '>':
            pos1 = cursor
            counter += 1
        if counter == n:
            return text[pos0+1:pos1]
        cursor += 1


while True:
    print('[{}] Monitoring latest update.'.format(get_date_string()))
    time_string = get_date_string()[:10]
    html = requests.get(url)
    html.encoding = 'utf-8'
    if time_string in html.text:
        idx = html.text.find(time_string)
        title = parse_title(html.text, idx, 5)
        if title not in lib: # and title not in tmplib:
            # start beeping thread
            thread = threading.Thread(target=beep, args=())
            thread.start()
            print("Update detected. Content")
            print("{}".format(title))
            print("Waiting for user's command to quit. Type y+ENTER to stop beeping.")
            # tmplib.append(title)

            cmd = input()
            thread.do_run = False
            thread.join()
            lib.append(title)
            # tmplib.remove(title)
            print("Update handled.")
    time.sleep(interval)

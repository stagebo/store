import os
import datetime
import time
import requests

def win_push(cmd):
    rel = os.system(cmd)
    print(cmd)


if __name__ == "__main__":
    win_push("git add .")
    win_push('git commit -m "script auto push, time %s"'%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    win_push('git push -u origin master')
    # try:
    #     requests.get("http://stagebo.xyz/admin/restart")
    # except:
    #     print("this code should be update to www.stagebo.xyz!")
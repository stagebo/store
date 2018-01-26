import time
import requests
import execjs

def statistics_number():
    req = requests.get('http://s13.cnzz.com/z_stat.php?id=1272819778&online=1&show=line')
    print(req)

    res = req.content.decode('utf-8')
    print(res)
    ret = execjs.eval(res)

    print(ret)




if __name__ == "__main__":
    statistics_number()
    pass
    print(execjs.eval("(function(){return 123;})()"))
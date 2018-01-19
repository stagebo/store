import redis
import  traceback
class RedisDb():

    def __init__(self):
        try:
            self.rd = redis.Redis(host="localhost",port=6379)
        except:
            traceback.print_exc()

    def reconn(self):
        try:
            self.rd = redis.Redis(host="localhost",port=6379)
        except:
            traceback.print_exc()

    def set(self,key,value,ex=None):
        if not ex:
            ex = 30*60
        self.rd.set(key,value,ex=ex)


    def get(self,key):
        return self.rd.get(key).decode('utf-8')

if __name__ == "__main__":
    rd = RedisDb()
    rd.set("name","wanyongbo")
    print(rd.get("name"))
    rd.rd.set


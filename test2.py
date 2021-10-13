import time

class Test():
    def __init__(self, id):
        self.id = id 
    
    def timeResume(self, second):
        print("start" + str(self.id))
        time.sleep(second)
        print("end" + str(self.id))
    
from concurrent.futures import ProcessPoolExecutor
import time

def timeResume(timeNum):
    print("Start")
    time.sleep(timeNum)
    print("End")

class Test():

    def call(self):
        with ProcessPoolExecutor(max_workers=2) as executor:
            future = executor.map(timeResume, 5)
        while True:
            print("wait...")
            if future.done():
                break

if __name__ == "__main__":
    t = Test()
    t.call()

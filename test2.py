import time
from multiprocessing import Pool, Process

def nijou(inputs):
    x = inputs
    print('input: %d' % x)
    time.sleep(2)
    retValue = x * x
    print('double: %d' % retValue)
    return(retValue)

if __name__ == "__main__":

    # Pool()を定義
    p = Pool()

    # プロセスを2つ非同期で実行
    result = p.apply_async(nijou, args=[3])
    result2 = p.apply_async(nijou, args=[5])

    # 1秒間隔で終了チェックして終了したら結果を表示
    for k in range(5):
        if result.ready():
            break
    print(result.get())
    print(result2.get())

    p.close()
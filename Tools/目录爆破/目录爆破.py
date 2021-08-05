# 1. 输入目标url和线程大小
# 2. 以队列的形式获取要爆破的路径
# 3. 定义路径获取函数get_path()
# 4. 利用多线程进行url目录爆破
# 5. 定义目录爆破函数get_url()

import urllib3
import queue
import threading
import sys
import time


def main(url, threadNum):
    # 2. 以队列的形式获取要爆破的路径
    path_queue = get_path(url)

    # 4. 利用多线程进行url目录爆破
    threads = []
    for i in range(threadNum):
        t = threading.Thread(target=get_url, args=(path_queue, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


# 5. 定义目录爆破函数get_url()
def get_url(path_queue):
    while not path_queue.empty():
        try:
            url = path_queue.get()
            http = urllib3.PoolManager()
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4549.400 QQBrowser/9.7.12900.400'}
            response = http.request('GET', url, headers=header)
            #print("[%d] = > %s" % (response.status, url))
            if response.status != 404:
                print("[%d] = > %s" % (response.status, url))
        except:
            pass
    else:
        sys.exit()


# 3. 定义路径获取函数get_path()
def get_path(url, file="G:/渗透/fuzz/Web-Fuzzing-Box-main/Dir/Directories.txt"):
    path_queue = queue.Queue()
    f = open(file, "r", encoding="gbk")
    for i in f.readlines():
        if i[0] == '/':
            i = i
        else:
            i = "/" + i
        path = url + i.strip()
        path_queue.put(path)
    f.close()
    return path_queue


if __name__ == "__main__":

    start = time.time()
    # 1. 输入目标url和线程大小
    url = input("Please input url:")
    if url[-1] == '/':
        url = url[:-1]
    else:
        url = url
    threadNum = int(input("Please input threads:"))
    main(url, threadNum)
    end = time.time()
    print("总共耗时 %.2f" % (end-start))

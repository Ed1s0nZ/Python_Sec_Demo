from threading import Thread
from queue import Queue
import requests


class UrlCheck(Thread):
    def __init__(self, url_queue, url_list):
        super().__init__()
        self.url_queue = url_queue  # 要探测的url队列
        self.url_list = url_list  # 存活的ip列表
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) '
                          'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                          'Version/13.0.3 Mobile/15E148 Safari/604.1'
        }

    def run(self):
        while True:
            try:
                url = self.url_queue.get()
                if 'http' in url:
                    head = self.download(url)
                    if head is None:
                        continue
                    self.url_list.append(url)
                    print(url, head)
                else:
                    http_url = 'http://' + url
                    head = self.download(http_url)
                    if head:
                        self.url_list.append(http_url)
                        print(http_url, head)
                    https_url = 'https://' + url
                    head = self.download(https_url)
                    if head is None:
                        continue
                    self.url_list.append(https_url)
                    print(https_url, head)
            finally:
                self.url_queue.task_done()

    def download(self, url):
        try:
            head = requests.get(url, headers=self.headers, timeout=3)
        except requests.RequestException:
            head = None
        return head


if __name__ == '__main__':
    u_queue = Queue()
    checker = [k.strip() for k in open('urls.txt', encoding='utf-8')]
    url_list = []
    save_name = "results.txt"  # 结果保存文件名
    for url in checker:
        u_queue.put(url)
    for i in range(50):
        bdm = UrlCheck(u_queue, url_list)
        bdm.daemon = True
        bdm.start()

    u_queue.join()

    f = open(save_name, mode='w', encoding='utf-8')
    for url in url_list:
        f.write(url+'\n')
    f.close()

    count = len(open(r"results.txt", 'rb').readlines())
    print('[*] 检测完成! 输入行数为>>' + str(count))
#   print(count)
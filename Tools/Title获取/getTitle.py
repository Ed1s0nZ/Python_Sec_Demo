import requests
import re
import csv
import threading
import urllib3
import queue
import sys
urllib3.disable_warnings()


def main(file,thread):
    url_list = get_path(file)
    threads = []
    for i in range(thread):
        t = threading.Thread(target=get_title, args=(url_list, ))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def get_title(url_list):
    while not url_list.empty():
        try:
            url = url_list.get()
            agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0'
            header = {'User-Agent': agent, 'Referer': url,'Connection': 'close', 'Accept-Language': 'zh-CN,zh;q=0.9','Cookie':'cookie2=dd;BAIDUID=249EA53D55EFB29293963959B7308217:FG=1'}
            r = requests.get(url, allow_redirects=False, timeout=15, headers=header, verify=False)  # verify ssl认证
            ctype = r.headers.get('Content-Type', 'n')
            if re.search(r'charset=("[^"<>\s]+"|[^"<>\s]+)', ctype):
                coding = re.findall(r'charset=("[^"<>\s]+"|[^"<>\s]+)', ctype)[0]
                coding = re.sub(r'\s|charset=|"', '', coding)
                r.encoding = coding
            elif re.search(r'charset=("[^"<>\s]+"|[^"<>\s]+)',r.text):
                coding = re.findall(r'charset=("[^"<>\s]+"|[^"<>\s]+)',r.text)[0]
                coding = re.sub(r'\s|charset=|"', '', coding)
                r.encoding = coding
            else:
                r.encoding = 'utf-8'
            body = r.text
            title = re.findall(r'<title>([\s\S]*?)</title>', body)
            title = dict(enumerate(title)).get(0, '-').replace('\n', '')
            code = r.status_code
            title_all.append([url, code, title])
            print([url, code, title])
        except Exception as e:
            print('请求错误')
    else:
        sys.exit()


def title_csv(saveTitle,title_all):
    with open(saveTitle, 'a', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(title_all)


def get_path(file):
    url_list = queue.Queue()
    f = open(file, "r", encoding="gbk")
    for i in f.readlines():
        path = i.strip()
        url_list.put(path)
    f.close()
    return url_list


if __name__ == "__main__":
    file="url_list.txt" # 存放url的txt
    saveTitle="saveTitle.csv" # 存放结果的csv
    thread=30 # 线程数
    title_all = []
    main(file,thread)
    title_csv(saveTitle,title_all)

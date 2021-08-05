import re


def compare():
    f = open("C:/Users/ThinkPad/Desktop/对比/b.txt", "r") # b 的路径
    lines = f.readlines()
    for i in lines:
        print(i.strip())
    f.close()


compare()


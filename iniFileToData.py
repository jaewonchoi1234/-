

import os



def extract_ssh_info(file_path):
    host = None
    port = None

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:

            if 'S:"Hostname"' in line:
                host = line.split('=')[1].strip()

            elif 'D:"[SSH2] Port"' in line:
                hex_port = line.split('=')[1].strip()
                port = int(hex_port, 16)   # hex → decimal 변환

            elif 'D:"Port"' in line:
                hex_port = line.split('=')[1].strip()
                port = int(hex_port, 16)   # hex → decimal 변환

    return host, port

import queue

path = "C:\\Users\\qwasz\\OneDrive\\pc_backup\\Config\\Sessions\\내 담당 원격점검 사이트 세션\\16. 화승인도네시아\\03"

session =[]

queue1 = queue.Queue()

list1 = os.listdir(path)
for file in list1:
    if file.endswith(".ini")and file!="__FolderData__.ini" and "자산아님" not in file:
        host,port=extract_ssh_info(path+'\\'+file)
        standpoint = {'host': host, 'port': port}
        session.append(standpoint)
    elif not file.endswith(".ini"):
        queue1.put(file)

while queue1.qsize() > 0:
    mother = queue1.get()
    list2 = os.listdir(path+'\\'+mother)
    for file in list2:
        if file.endswith(".ini") and file!="__FolderData__.ini" and "자산아님" not in file:
            host, port = extract_ssh_info(path + '\\' +mother +'\\'+file)
            standpoint = {'host': host, 'port': port}
            session.append(standpoint)
        elif not file.endswith(".ini"):
            queue1.put(mother+"\\"+file)


print(len(session))


print(session)







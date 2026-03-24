# 샘플 Python 스크립트입니다.

# Shift+F10을(를) 눌러 실행하거나 내 코드로 바꿉니다.
# 클래스, 파일, 도구 창, 액션 및 설정을 어디서나 검색하려면 Shift 두 번을(를) 누릅니다.

from datetime import datetime
import queue
import os
import telnetlib3
import asyncio
import asyncssh


def extract_ssh_info(file_path):
    host = None
    port = None
    protocol = None
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

            elif 'S:"Protocol Name"' in line:
                protocol = line.split('=')[1].strip()

    return host, port, protocol

def extract_ssh_session(file_path):

    session =[]

    queue1 = queue.Queue()

    list1 = os.listdir(file_path)
    for file in list1:
        if file.endswith(".ini")and file!="__FolderData__.ini" and "자산아님" not in file:
            host,port,protocol=extract_ssh_info(file_path+'\\'+file)
            standpoint = {'host': host, 'port': port, 'protocol': protocol}
            session.append(standpoint)
        elif not file.endswith(".ini"):
            queue1.put(file)

    while queue1.qsize() > 0:
        mother = queue1.get()
        list2 = os.listdir(file_path+'\\'+mother)
        for file in list2:
            if file.endswith(".ini") and file!="__FolderData__.ini" and "자산아님" not in file:
                host, port,protocol = extract_ssh_info(file_path + '\\' +mother +'\\'+file)
                standpoint = {'host': host, 'port': port, 'protocol': protocol}
                session.append(standpoint)
            elif not file.endswith(".ini"):
                queue1.put(mother+"\\"+file)

    return session


def remoteInspection(session):
    #tatadaewoo
    username = 'tdcv123'
    password = ''


    today = datetime.today().strftime('%Y%m%d')
    os.mkdir('./logs/' + today)
    #세션 접속
    for session in session:
        if session['protocol'] == 'SSH2':

            #ssh 접속
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(session['host'],session['port'],username,password)

            # sh run에서 banner 찾아서 출력값에서 banner 뺴기
            stdin, stdout, stderr = client.exec_command('show run')
            text = stdout.read().decode('utf-8')
            banner_index = text.find('banner motd ^C')+15
            banner = text[banner_index:].split('^C')[0].strip()
            no_banner = text[text.find(banner)+len(banner):]

            # hostname 찾기
            hostname_index=no_banner.find('hostname')+9
            if hostname_index!=8:
             hostname = no_banner[hostname_index:].split('\n')[0].strip()
            else:
             hostname = 'unknown'

            # 파일 생성
            file_name= session['host']+hostname+datetime.now().strftime("_%Y-%m-%d_%H:%M:%S")
            file = open("./logs/"+today+'/'+file_name,'w')

            # ssh 명령어 입력 및 결과값 파일에 쓰기
            command = ['sh process cpu','sh process m','sh mac add','sh cdp nei','sh cdp nei de','sh arp','sh span','sh ip int bri','sh ip route','sh ip route sum','dir','sh etherch sum'
                      ,'sh inter status','sh inter count','sh inter count error','sh run','sh clock','sh log','sh ver','sh env all','sh clock','sh int status | inc err']
            for command in command:
                stdin, stdout, stderr = client.exec_command(command)
                text = stdout.read().decode('utf-8')
                file.write(hostname+'#'+command+'\n')
                file.write(text)
        elif session['protocol'] == 'Telnet':
            =telnetlib3.open_connection(session['host'],session['port'])


if __name__ == '__main__':
    path = "C:\\Users\\qwasz\\OneDrive\\pc_backup\\Config\\Sessions\\내 담당 원격점검 사이트 세션\\16. 화승인도네시아\\03"
    session=extract_ssh_session(path)
    remoteInspection(session)


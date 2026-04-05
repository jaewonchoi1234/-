from datetime import datetime
import queue
import os
import asyncssh
import pandas as pd



#세션 가져오기 csv
def get_session_from_csv(filename):
    df = pd.read_csv(filename)
    return df['host']

def connect_ssh(df):
    


def parse_result():



def make_logfile():



def check_hardware():



def print_log():



def compare_result():



def make_report():





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


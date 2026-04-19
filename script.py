from datetime import datetime
import os
import asyncssh
import pandas as pd
import asyncio
import sys


def get_command_from_txt(path):
    commands=[]
    with open(path,'r',encoding="utf-8") as f:
        lines = f.readlines
        for line in lines:
            commands.append(line.strip())
    return commands
        

#세션 가져오기 csv
def get_session_from_csv(filename):
    df = pd.read_csv(filename)
    return df['host'].tolist()


async def run_client(host,commands):
    result = []
    async with asyncssh.connect(host) as conn:
        for command in commands:
            result.append(await conn.run(command))
        return result


async def run_clients(session,commands):
    results = []
    for host in session:
       try:
            asyncio.get_event_loop().run_until_complete(run_client())
       except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))
       await results.append(run_client(host,commands))
    return results


def parse_result(result):
    result.stdout


def make_logfile():



def check_hardware():



def print_log():



def compare_config():



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
            
            for command in command:
                stdin, stdout, stderr = client.exec_command(command)
                text = stdout.read().decode('utf-8')
                file.write(hostname+'#'+command+'\n')
                file.write(text)
        elif session['protocol'] == 'Telnet':
            =telnetlib3.open_connection(session['host'],session['port'])


if __name__ == '__main__':
    commands = get_command_from_txt('command')
    session = get_session_from_csv('csv/tata_csv')
    results = run_clients(session,commands)



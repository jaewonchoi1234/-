import os
import pandas as pd
import queue


#ini파일에서 host 추출
def extract_host_info(file_path):
    host = None
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if 'S:"Hostname"' in line:
                host = line.split('=')[1].strip()
    return host

#디렉토리에서 ini파일 탐색
def explore_ini(file_path, q, session):
        list1 = os.listdir(file_path)
        for file in list1:
            path =file_path+'/'+file
            if file.endswith(".ini") and file!="__FolderData__.ini" and "자산아님" not in file:
                host=extract_host_info(path)
                session.append(host)
            elif os.path.isdir(path):
                q.put(file_path+'/'+file)
        return q

#ini 파일에서 세션 가져오기
def get_session_from_ini(file_path):
    session =[]
    queue1 = queue.Queue()
    
    explore_ini(file_path, queue1,session)
    while queue1.qsize() > 0:
        explore_ini(queue1.get(), queue1,session)


    return session


#csv 세션 파일 만들기
def make_csv_session(session, file_name):
    data = {'host': session}
    df = pd.DataFrame(data)
    os.makedirs("csv", exist_ok=True)
    if os.path.exists("csv/"+file_name):
        raise FileExistsError(f"{file_name}은 이미 존재합니다.")
    df.to_csv('csv/'+file_name+'.csv')



file_name = "tata_csv"
file_path = "ini/03"
session = get_session_from_ini(file_path)
make_csv_session(session, file_name)

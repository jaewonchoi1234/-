import asyncssh
import pandas as pd
import asyncio
import os



def get_command_from_txt(path):
    commands=[]
    with open(path,'r',encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            commands.append(line.strip())
    return commands
        

#세션 가져오기 csv
def get_session_from_csv(filename):
    df = pd.read_csv(filename)
    return df['host'].tolist()


async def run_client(host,commands):
    result = []
    async with sem:
        try:
            async with asyncssh.connect(host,username="tdcv123",password="MISgortla~09") as conn:
                for command in commands:
                    try:
                        r=await conn.run(command)
                        result.append({'command':command,'result':r.stdout, 'success': True})
                    except Exception as e:
                        result.append({'command':command,'result':str(e), 'success': False, 'host': host})
        except Exception as e:
            result.append({'result':str(e), 'success': False, 'host': host})
        return result


async def run_clients(session,commands):
    tasks = [run_client(host, commands) for host in session]
    result = await asyncio.gather(*tasks)
    success_list = [r for r in result if r['success'] == True]
    fail_list = [r for r in result if r['success'] == False]
    return success_list, fail_list


def make_csv_session(session, file_name):
    data = {'host': session}
    df = pd.DataFrame(data)
    os.makedirs("csv", exist_ok=True)
    if os.path.exists("csv/"+file_name):
        raise FileExistsError(f"{file_name}은 이미 존재합니다.")
    df.to_csv('csv/'+file_name+'.csv')


#def parse_result(results, lenth):
 #   #for result in results:
  #      for i in range(0,lenth-1):
   #         print(results[i])


#def make_logfile():



#def check_hardware():



#def print_log():



#def compare_config():



#def make_report():



if __name__ == '__main__':
    commands = get_command_from_txt('commands/command.txt')
    session = get_session_from_csv('csv/tata_csv.csv')
    sem = asyncio.Semaphore(25)
    success_list , fail_list = run_clients(session,commands)
    make_csv_session([fail['host'] for fail in fail_list], 'csv/tata_fail.csv')
   # parse_result(results,len(commands))


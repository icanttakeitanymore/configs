#!/usr/bin/env python3
# Сканер публичных фтп.
import subprocess
import ftplib
import sys

nmap = '/usr/bin/nmap'    # Бинарник nmap.
nmap_arg1= '-sP'          # Проверка пингом.
nmap_arg2= '-p 21'        # Порт 21.
ip = str(sys.argv[1]) + '/24'   # Сканируемая сеть.

servers_found_nmap = []   # Лист полученый с stdout nmap.
servers_found_instr = []  # Лист в котором происходит парсинг.
servers_found_online = [] # Лист хостов находящихся в сети.
servers_with_ftp = []     # Лист хостов с открытым портом.
servers_with_anon = []    # Логин анонимусом возвращает 230.

print("Сканируемая сеть: ", ip)


def network_scan():
    """Функция сканирования сети.
    Нмап сканирует сеть, список servers_found_nmap
    получает выдачу с stdout программы nmap, выбирается 
    столбец с ip в список servers_found_instr.
    """
    print("Поиск онлайн хостов.")
    job = subprocess.Popen([nmap,nmap_arg1,ip],stdout=subprocess.PIPE)
    out = job.communicate()
    
    for line in list(str(out).split("\\")):
        servers_found_nmap.append(line.split(" ")[-1::])
        
    
    # Выбор только тех строк в которых есть совпадения по ip[:10:], то есть 123.123.123.
    for i in servers_found_nmap:
        if str(i).find(ip[:10:]) != -1:
            servers_found_instr.append(i)
            
            
def converter(): 
    """Функция обработки списка servers_found_instr.
    Убираем лишние скобки и кавычки, получаем чистый список
    servers_found_online.
    """
    global servers_found_instr,servers_found_online
    servers_found_instr = str(servers_found_instr).replace(']]',']')
    servers_found_instr = str(servers_found_instr).replace('[[','[')
    servers_found_instr = str(servers_found_instr).replace('(','')
    servers_found_instr = str(servers_found_instr).replace(')','')
    servers_found_instr = str(servers_found_instr).replace('[','') 
    servers_found_instr = str(servers_found_instr).replace(']','')
    servers_found_instr = str(servers_found_instr).replace("'","")
    servers_found_instr = str(servers_found_instr).replace(" ","")
    servers_found_online = list(servers_found_instr.split(','))

    if servers_found_online == [""]:
        print("Нет онлайн хостов")
        sys.exit()
    
    for i in servers_found_online:
        print("Онлайн :", i)
                 
        
def port_scaner():
    """Функция сканирования порта в аргументе nmap_arg2.
    Помещаем хосты с открытым портом в servers_with_ftp.
    """
    length_servers_found_online = len(servers_found_online)
    print("Хостов обнаружено: ",length_servers_found_online)
    for i in servers_found_online:
        progress = servers_found_online.index(i)/(length_servers_found_online/100)
        print(i, int(progress), "%")
        job = subprocess.Popen([nmap, nmap_arg2, i],stdout=subprocess.PIPE)
        out = job.communicate()
        if str(out).find('STATE') != -1:    # Ищем STATE в выдаче nmap
            if str(out).find('open') != -1: # Ищем open в выдаче nmap
                servers_with_ftp.append(i)        # Если всё верно помещаем в список.
       


def try_to_connect():
    """Функция попытки соединения анонимным юзером
    Сохранение ls с фтп в файл с IP хоста в имени.
    """
    global servers_with_anon
    for i in servers_with_ftp:
        try:                    # Попытка обработки исключения в цикле.
            print("Тест:",i)
            ftp = ftplib.FTP(i)
            test = ftp.login()
            if test.split(" ")[0] == str(230):
                servers_with_anon.append(i)
                filename = str(i)+str('.ftplist')
                outfile = open(filename,'w')
                ftp.retrlines('LIST',lambda line, w=outfile.write: w(line+"\n"))
                print("Листинг файлов записан в : ",filename)
            else:
                continue
        except EOFError:        
            print("EOFError")
            continue
        except ftplib.error_perm as e:
            print(e)
            continue

# Runc

network_scan()
converter()


port_scaner()

for i in servers_with_ftp:
    print(i, " Открыт")
    
try_to_connect()

if servers_with_ftp == []:
    print("В этом диапазоне нет открытых фтп")
else:
    output = open('output.txt', 'w')
    output.write(str(servers_with_anon))
    output.close()

for i in servers_with_anon:
    print(i, " Анонимное соединение")

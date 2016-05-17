#!/usr/bin/env python3
# Сканер публичных фтп.
import subprocess
import ftplib
import sys
import os

nmap = '/usr/bin/nmap'    # Бинарник nmap.
nmap_arg1= '-sP'          # Проверка пингом.
nmap_arg2= '-p 21'        # Порт 21.


servers_found_nmap = []   # Лист полученый с stdout nmap.
servers_found_instr = []  # Лист в котором происходит парсинг.
servers_found_online = [] # Лист хостов находящихся в сети.
servers_with_ftp = []     # Лист хостов с открытым портом.
servers_with_anon = []    # Логин анонимусом возвращает 230.




def network_scan():
    """Функция сканирования сети.
    Нмап сканирует сеть, список servers_found_nmap
    получает выдачу с stdout программы nmap, выбирается 
    столбец с ip в список servers_found_instr.
    """
    print("[ Поиск онлайн хостов. ]")
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
    servers_found_online = servers_found_instr.split(',')

    if servers_found_online == []:
        print("Нет онлайн хостов")
        sys.exit()

    print("Сервера онлайн: ", servers_found_online)



def port_scaner():
    """Функция сканирования порта в аргументе nmap_arg2.
    Помещаем хосты с открытым портом в servers_with_ftp.
    """
    print("\n[ Полверка 21 порта началась. ]")
    length_servers_found_online = len(servers_found_online)
    print("[ Хостов обнаружено: ",length_servers_found_online,"]")
    for i in servers_found_online:
        progress = servers_found_online.index(i)/(length_servers_found_online/101)
        print("[", '-'*int(progress), " "*int(101 - int(progress)), int(progress),"%","]",i, end='')
        print('\r' * 110, end='')
        if int(progress) == 100:
            print("\n[ Полверка 21 порта окончена. ]")
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
            print("Тест анонимного соединения:",i)
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
if __name__ == '__main__':
	try:
		ip = str(sys.argv[1]) + '/24'   # Сканируемая сеть.
		if os.getuid() != 0:
			print('Необходимы права суперпользователя')
			os.exit()
		else:
			print("[ Сканируемая сеть: ", ip,"]")
			network_scan()
			converter()
			port_scaner()

			for i in servers_with_ftp:
				print("\n", i, " Открыт")

			try_to_connect()

			if servers_with_ftp == []:
				print("\nВ этом диапазоне нет хостов с открытым 21 портом")
			else:
				output = open('output.txt', 'w')
				output.write(str(servers_with_anon))
				output.close()

			for i in servers_with_anon:
				print(i, " Анонимное соединение")
	except IndexError:
		print("""
			Необходимо указать сканируемую сеть
			например 192.168.1.0 или 10.100.1.0.
			Сети сканируются по маске /24.
			""")
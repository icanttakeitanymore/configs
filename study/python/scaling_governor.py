#!/usr/bin/env python3
# Переключение режимов скейлинга частоты процессора.
#
# governor - Режим.
# scaling_available_governors - Файл в котором хранятся доступные режимы.
# scaling_governor_working - Файл текущего режима.
#
# root@notebook:/home/boris/study/python# ./cpufreq.py 
# (0, 'performance')
# (1, 'powersave')
# Ядер у процессора : 2
# Введите номер требуемого режима ::0
# Ядру  0 установлен режим performance
# Ядру  1 установлен режим performance
# root@notebook:/home/boris/study/python#
import os,sys
# Выбор режима.
def select_governors():
    """Функция выбора режима"""
    global governor,cpu_cores_val
    #Получение доступных режимов.
    scaling_available_governors = str(open('/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors').readline()).rstrip().rsplit(" ")
    #Вывод на экран.
    for i in enumerate(scaling_available_governors):
        print(i)
    #Получение количества процессоров.
    for line in open('/proc/cpuinfo').readlines():
        if line.find('cpu cores') == 0:
            cpu_cores = line.rstrip().rsplit(":")
            cpu_cores_val = int(cpu_cores[1].replace(" ",""))
            break
    print("Ядер у процессора :", cpu_cores_val)
    #Выбор нужного режима.
    governor_num = int(input("Введите номер требуемого режима ::"))
    governor = scaling_available_governors[governor_num]

    
# Установка значений 
def scaling_write(governor):
    """Функция установки значения скейлинга"""
    for i in range(cpu_cores_val):
        scaling_governor_working = '/sys/devices/system/cpu/cpu%d/cpufreq/scaling_governor' % i  # Файлы для ядер в разных каталогах.
        action_scaling_governors = open(scaling_governor_working, 'w')
        action_scaling_governors.write(governor)
        action_scaling_governors.close()
        print("Ядру ", i , "установлен режим", governor)



                   
                   
# Ошибки. 
def run():
    try:
        select_governors()
    except ValueError:
        print("Ошибка в select_governors(): Не верное значение номера режима")
    except IndexError:
        print("Ошибка в select_governors(): Значение не входит номера допустимых режимов")
    try:
        scaling_write(governor)
    except NameError:
        print("Ошибка в scaling_write(governor): Исполнение не возможно")
    except PermissionError:
        print("Ошибка в scaling_write(governor): Нет доступа к /sys")
        
# Запуск.
if __name__ == '__main__':
    if os.getuid() != 0:
        print("Необходимо выполнять с правами суперпользователя")
        sys.exit()
    else:
        run()

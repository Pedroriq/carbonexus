import components.component as comp
import cpuinfo
import pandas as pd
import psutil
from threading import Thread
import subprocess


def get_measurents():
    mean_list = []
    while True:
        cpu_usage = process.cpu_percent(interval=1)
        mean_list.append(cpu_usage)
        print(len(mean_list))
        if len(mean_list) == 60:
            mean = sum(mean_list)/len(mean_list)
            print(f"Essa é a media: {mean}")
            mean_list = []


def traine():
    while True:
        pass


cpu = comp.get_cpu_information()

cpu_voltage_file = pd.read_csv('files/processors_core.csv', sep=";")

brand = cpu.split()[0]
product_line = cpu.split()[1]
model = cpu.split()[2]

if "core" in product_line.lower():
    consume = cpu_voltage_file[cpu_voltage_file['processor_number'] == model]['TDP']
    print(consume)

current_process = psutil.Process()
print(current_process.pid)
process = psutil.Process(current_process.pid)

thread = Thread(target=get_measurents)
thread2 = Thread(target=traine)

thread.start()
thread2.start()

thread.join()

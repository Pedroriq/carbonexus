import os.path

import app.measurement.components.component as comp
import pandas as pd
import psutil
from threading import Thread, Event


class CpuMeasurement(Thread):

    def __init__(self):
        super().__init__()
        self.tdp = None
        self.process = None
        self.event = Event()
        self.start_informations()
        self.start()


    def run(self):
        self.event.wait()
        self.get_measurents(self.process)


    def start_informations(self):
        print('Iniciando coleta das infos da CPU')
        basepath = os.path.dirname(__file__)
        file_path = os.path.abspath(os.path.join(basepath, 'file', 'processors_core.csv'))

        cpu = comp.get_cpu_information()

        cpu_voltage_file = pd.read_csv(file_path, sep=";")

        self.tdp = cpu_voltage_file[cpu_voltage_file['PROCESSOR'] == cpu]['TDP']

        current_process = psutil.Process()
        print(current_process.pid)
        self.process = psutil.Process(current_process.pid)

        print("INFOS CPU OK")


    @staticmethod
    def get_measurents(process):
        mean_list = []
        while True:
            cpu_usage = process.cpu_percent(interval=1)
            print(f"USO DA CPU: {cpu_usage}")
            mean_list.append(cpu_usage)


    def start_measurent(self):
        self.event.set()

    def stop_measurent(self):
        self.event.clear()

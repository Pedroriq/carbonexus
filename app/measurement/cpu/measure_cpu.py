import os.path
import time

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
        self.get_measurents()


    def start_informations(self):
        print('Iniciando coleta das infos da CPU')
        basepath = os.path.dirname(__file__)
        file_path = os.path.abspath(os.path.join(basepath, 'file', 'processors_core.csv'))

        cpu = comp.get_cpu_information()

        cpu_voltage_file = pd.read_csv(file_path, sep=";")

        self.tdp = cpu_voltage_file[cpu_voltage_file['PROCESSOR'] == cpu]['TDP']

        print("INFOS CPU OK")

    def get_measurents(self):
        while self.process.is_running():
            try:
                num_cores = psutil.cpu_count()
                children = self.process.children(recursive=True)
                if len(children) != 0:
                    for child in children:
                        self.measure_cpu(child, num_cores)
                else:
                    self.measure_cpu(self.process, num_cores)
            except Exception as e:
                pass
        self.stop_measurent()

    def measure_cpu(self, process, num_cores):
        cpu_usage = process.cpu_percent(interval=1)
        print(f"USO DA CPU: {cpu_usage / num_cores}")
        return cpu_usage / num_cores

    def start_measurent(self, process_id):
        self.process = psutil.Process(process_id)
        self.event.set()

    def stop_measurent(self):
        self.event.clear()

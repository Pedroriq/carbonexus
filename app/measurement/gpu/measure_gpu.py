from threading import Thread, Event

import pynvml
import time


class GpuMeasurement(Thread):

    def __init__(self):
        super().__init__()
        pynvml.nvmlInit()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        self.event = Event()
        self.start()
        self.total_energy = 0

    def run(self):
        self.event.wait()
        while True:
            self.total_energy += pynvml.nvmlDeviceGetPowerUsage(self.handle) / 1000
            time.sleep(1)
            print(f'{"{:.7f}".format(self.total_energy / (1000 * 3600))} kWh')

    def start_measurent(self):
        self.event.set()

    def stop_measurent(self):
        pynvml.nvmlShutdown()
        self.event.clear()
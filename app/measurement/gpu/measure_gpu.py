import time
from threading import Event, Thread

import psutil
import pynvml


class GpuMeasurement(Thread):

    def __init__(self):
        super().__init__()
        pynvml.nvmlInit()
        self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        self.event = Event()
        self.total_energy = 0
        self.process = None
        self.start()

    def run(self):
        self.event.wait()
        while self.process.is_running():
            self.total_energy += (
                pynvml.nvmlDeviceGetPowerUsage(self.handle) / 1000
            )
            time.sleep(1)
            print(
                f'USO DA GPU {"{:.7f}".format(self.total_energy / (1000 * 3600))} kWh'
            )
        return

    def start_measurent(self, process_id):
        self.process = psutil.Process(process_id)
        self.event.set()

    def stop_measurent(self):
        pynvml.nvmlShutdown()
        self.event.clear()

    @property
    def total_energy_gpu(self):
        return self.total_energy / (1000 * 3600)

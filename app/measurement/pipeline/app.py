import time
from datetime import datetime
from threading import Thread
from app.measurement.github.github import Repository
from app.measurement.cpu.measure_cpu import CpuMeasurement
from app.measurement.gpu.measure_gpu import GpuMeasurement
from app.measurement.code_runner.runner import Runner
from app.utils.energy_consume import calculate_kwh


class Pipeline(Thread):
    def __init__(self, git_url, country):
        super().__init__()

        time.sleep(5)

        Repository(git_url).start()

        processor = CpuMeasurement()
        graphic_driver = GpuMeasurement()
        code = Runner()

        start_time = datetime.now()
        code.start_code(processor, graphic_driver)
        code.join()
        end_time = datetime.now()

        total_time = (end_time - start_time).total_seconds() / 3600

        calculate_kwh(processor.get_tdp, graphic_driver.total_energy_gpu, total_time)
        



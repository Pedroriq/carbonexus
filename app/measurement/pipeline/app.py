import time
from threading import Thread
from app.measurement.github.github import Repository
from app.measurement.cpu.measure_cpu import CpuMeasurement
from app.measurement.gpu.measure_gpu import GpuMeasurement
from app.measurement.code_runner.runner import Runner


class Pipeline(Thread):
    def __init__(self, git_url, country):
        super().__init__()

        time.sleep(5)

        Repository(git_url).start()

        processor = CpuMeasurement()
        graphic_driver = GpuMeasurement()
        code = Runner()

        process_id = code.start_code(processor, graphic_driver)


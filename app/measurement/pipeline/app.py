from threading import Thread
from measurement.github.github import Repository
from measurement.cpu.measure_cpu import CpuMeasurement
from measurement.gpu.measure_gpu import GpuMeasurement


class Pipeline(Thread):
    def __init__(self, git_url, country):
        super().__init__()

        Repository(git_url).start()

        processor = CpuMeasurement()
        graphic_driver = GpuMeasurement()

        processor.start_measurent()
        graphic_driver.start_measurent()


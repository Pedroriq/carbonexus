from threading import Thread, Event
import os
import platform
import subprocess


class Runner(Thread):
    def __init__(self):
        super().__init__()
        self.graphic_driver = None
        self.processor = None
        self.runner_event = Event()
        self.start()

    def run(self):
        self.runner_event.wait()
        self.run_code()


    def run_code(self):
        actual_dir = os.getcwd()
        repository_dir = os.path.join(actual_dir, 'repository_git')

        os.chdir(repository_dir)
        if platform.system() == "Windows":
            python_executable = os.path.join(repository_dir, 'venv', 'Scripts', 'python.exe')
            process = subprocess.Popen([python_executable, "main.py"], shell=False)
        elif platform.system() == "Linux":
            python_executable = os.path.join(repository_dir, 'venv', 'bin', 'python')
            process = subprocess.Popen([python_executable, "main.py"])

        os.chdir(actual_dir)

        self.processor.start_measurent(process.pid)
        self.graphic_driver.start_measurent(process.pid)

        # self.processor.join()
        # self.graphic_driver.join()
        # self.join()

        return process.pid

    def start_code(self, processor, graphic_driver):
        self.processor = processor
        self.graphic_driver = graphic_driver
        self.runner_event.set()

    def stop_code(self):
        self.runner_event.clear()
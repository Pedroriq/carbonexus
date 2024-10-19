import platform
import psutil
import GPUtil
import cpuinfo


def get_system_information():
    system_info = platform.uname()

    print("System Information:")
    print(f"System: {system_info.system}")
    print(f"Node Name: {system_info.node}")
    print(f"Release: {system_info.release}")
    print(f"Version: {system_info.version}")
    print(f"Machine: {system_info.machine}")
    print(f"Processor: {system_info.processor}")


def get_cpu_information():
    cpu_info = cpuinfo.get_cpu_info()
    cpu_model = cpu_info['brand_raw']
    return cpu_model


def get_memory_information():
    memory_info = psutil.virtual_memory()

    print("\nMemory Information:")
    print(f"Total Memory: {memory_info.total} bytes")
    print(f"Available Memory: {memory_info.available} bytes")
    print(f"Used Memory: {memory_info.used} bytes")
    print(f"Memory Utilization: {memory_info.percent}%")


def get_disk_information():
    disk_info = psutil.disk_usage('/')

    print("\nDisk Information:")
    print(f"Total Disk Space: {disk_info.total} bytes")
    print(f"Used Disk Space: {disk_info.used} bytes")
    print(f"Free Disk Space: {disk_info.free} bytes")
    print(f"Disk Space Utilization: {disk_info.percent}%")


def get_gpu_information():
    gpus = GPUtil.getGPUs()

    if not gpus:
        print("No GPU detected.")
    else:
        for i, gpu in enumerate(gpus):
            print(f"\nGPU {i + 1} Information:")
            print(f"ID: {gpu.id}")
            print(f"Name: {gpu.name}")
            print(f"Driver: {gpu.driver}")
            print(f"GPU Memory Total: {gpu.memoryTotal} MB")
            print(f"GPU Memory Free: {gpu.memoryFree} MB")
            print(f"GPU Memory Used: {gpu.memoryUsed} MB")
            print(f"GPU Load: {gpu.load * 100}%")
            print(f"GPU Temperature: {gpu.temperature}°C")

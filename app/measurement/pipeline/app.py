import sys
import time
from datetime import datetime
from threading import Thread

from app.api.api import ElectricityAPI
from app.measurement.code_runner.runner import Runner
from app.measurement.cpu.measure_cpu import CpuMeasurement
from app.measurement.github.github import Repository
from app.measurement.gpu.measure_gpu import GpuMeasurement
from app.utils.energy_consume import EnergyConsumption
from app.utils.verify_country import get_zone_code


class Pipeline(Thread):
    def __init__(self, git_url, country, result_queue):
        super().__init__()

        time.sleep(5)
        zone_code = get_zone_code(country)
        carbon_intensity_country = ElectricityAPI().get_carbon_intensity_api(
            f"v3/carbon-intensity/latest?countryCode={zone_code}"
        )

        if not zone_code or not carbon_intensity_country:
            time.sleep(10)
            sys.exit()

        Repository(git_url).start()

        processor = CpuMeasurement()
        graphic_driver = GpuMeasurement()
        code = Runner()

        start_time = datetime.now()
        code.start_code(processor, graphic_driver)
        code.join()
        end_time = datetime.now()

        total_time = (end_time - start_time).total_seconds() / 3600

        energy_consumption = EnergyConsumption()
        energy_consumption.calculate_kwh(
            processor.get_tdp, graphic_driver.total_energy_gpu, total_time
        )
        co2_eq = energy_consumption.calculate_carbon_intensity(
            carbon_intensity_country
        )

        result_co2 = round(co2_eq, 4)
        result_co2_kg = result_co2 / 1000
        result_queue.put(result_co2_kg)

        print(f"QUANTIDADE DE CARBONO EMITIDO: {result_co2}g")

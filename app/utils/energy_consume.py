import pandas as pd
from app.api.api import ElectricityAPI


class EnergyConsumption:
    def __init__(self):
        self.total_consumption = None

    def calculate_kwh(self, tdp, total_energy_gpu, time_consume):
        pue = 1.09
        file_cpu_usage = pd.read_csv("app/measurement/test_result/test.csv")
        mean_cpu_percent = file_cpu_usage["cpu_usage"].mean()
        mean_cpu = mean_cpu_percent / 100
        cpu_consumption_kwh = (mean_cpu * tdp) / 1000
        self.total_consumption = (cpu_consumption_kwh + total_energy_gpu) * pue * time_consume
        print(f'TOTAL USE: {"{:.7f}".format(self.total_consumption)} kW')
    
    def calculate_carbon_intensity(self, carbon_intensity_country):
        return self.total_consumption * carbon_intensity_country
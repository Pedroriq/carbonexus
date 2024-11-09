import pandas as pd


def calculate_kwh(tdp, total_energy_gpu, time_consume):
    pue = 1.09
    file_cpu_usage = pd.read_csv("app/measurement/test_result/test.csv")
    mean_cpu_percent = file_cpu_usage["cpu_usage"].mean()
    mean_cpu = mean_cpu_percent / 100
    cpu_consumption_kwh = (mean_cpu * tdp) / 1000
    total_consumption = (cpu_consumption_kwh + total_energy_gpu) * pue * time_consume
    print(f'TOTAL USE: {"{:.7f}".format(total_consumption)} kW')

import numpy as np
import csv

n = []
temp = []
humi = []

with open('sensordata.txt','r') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        n.append(int(row[0]))
        temp.append(int(row[1]))
        humi.append(int(row[2]))

mean_temp = np.mean(temp)
_________________________ #compute mean humidity
print("The means are ", int(mean_temp), " deg C and ", int(mean_humi), "%")

median_temp = np.median(temp)
median_humi = np.median(humi)
print("The medians are ", int(median_temp), " deg C and ", int(median_humi), "%")

min_temp = np.min(temp)
min_humi = np.min(humi)
print("The minimums are ", int(min_temp), " deg C and ", int(min_humi), "%")

max_temp = np.max(temp)
max_humi = np.max(humi)
print("The maximums are ", int(max_temp), " deg C and ", int(max_humi), "%")

var_temp = np.var(temp)
var_humi = np.var(humi)
print("The variances are ", int(var_temp), " deg C and ", int(var_humi), "%")

std_temp = np.std(temp)
_______________________ #compute standard deviation for humidity
print("The standard deviations are ", int(std_temp), " deg C and ", int(std_humi), "%")

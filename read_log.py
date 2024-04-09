import pandas as pd

batchs = []
plugins = []
throughputs = []
memory_usages = []

with open('log.txt', 'r') as file:
    lines = file.readlines()
    for i in range(len(lines)):
        if 'batch size per gpu' in lines[i]:
            line = lines[i].strip() + lines[i+1].strip() + lines[i+2].strip()
            batch, plugin, throughput, memory = line.split(',')
            batch = int(batch.split()[-1][7:][:-4])
            plugin = plugin.split()[-1]
            throughput = float(throughput.split()[-1][7:][:-4])
            memory_unit = memory.split()[-1][:-1]
            memory_usage = float(memory.split()[-2][7:][:-4])
            #print(batch, plugin, throughput)
            if memory_unit == 'MB':
                memory_usage /= 1024
            #print(memory_unit, memory_usage)
            batchs.append(batch)
            plugins.append(plugin)
            throughputs.append(throughput)
            memory_usages.append(memory_usage)

test_log = pd.DataFrame({'batch': batchs, 'plugin': plugins, 'throughput':throughputs, 'memory_usage_per_gpu(GB)':memory_usages})
test_log.to_csv('benchmark.csv')
test_log

import seaborn as sns
import matplotlib.pyplot as plt
sns.set_style('whitegrid')
plt.figure(figsize=(9, 6))
sns.barplot(x='batch', y='throughput', hue='plugin', data=test_log)
plt.title('throughput via different plugin')
plt.savefig('throughput.png')

sns.set_style('whitegrid')
plt.figure(figsize=(9, 6))
sns.barplot(x='batch', y='memory_usage_per_gpu(GB)', hue='plugin', data=test_log)
plt.title('memory usage via different plugin')
plt.savefig('memory.png')
